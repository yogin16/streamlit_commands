import importlib
from glob import glob
from importlib import util
from os.path import dirname, basename, isfile

import streamlit as st

from command import registered_commands


def load_module(_module):
    importlib.import_module(_module)
    loader = importlib.util.find_spec(_module).loader
    all_modules = [
        basename(f)[:-3]
        for f in glob(dirname(loader.get_filename()) + "/*.py")
        if isfile(f) and not f.endswith("__init__.py")
    ]
    for mod_ in all_modules:
        importlib.import_module("." + mod_, _module)


load_module('commands')


def build_form(fields, context):
    for field in fields:
        label = field["name"]
        field_type = field["type"]
        value = None
        if "text" == field["type"]:
            value = st.text_input(label)
        if "text_area" == field["type"]:
            value = st.text_area(label)
        if "selectbox" == field_type:
            value = st.selectbox(label, field["options"])
        if "fields" not in context:
            context["fields"] = []
        context["fields"].append({"key": label, "value": value})


def params(context):
    rv = {}
    for field in context["fields"]:
        k = field["key"]
        v = field["value"]
        rv[k] = v
    return rv


def render(result):
    if "text" == result.type:
        st.write(result.payload)
    if "markdown" == result.type:
        st.markdown(result.payload)
    if "json" == result.type:
        st.json(result.payload)
    if "graphviz" == result.type:
        st.graphviz_chart(result.payload)
    if "html" == result.type:
        st.write(result.payload, unsafe_allow_html=True)
        if result.extra_json:
            st.json(result.extra_json)


def main():
    commands = registered_commands()
    st.sidebar.header("""
    Streamlit Admin Console
    """)
    command_key = st.sidebar.selectbox("🛠 Choose the command", [c for c in commands.keys()])

    command = commands[command_key]

    context = {}
    st.header(command.title())
    st.markdown(command.description())
    build_form(command.form_fields(), context)

    if st.button('Submit'):
        result = command.execute(params(context))
        render(result)


if __name__ == '__main__':
    main()

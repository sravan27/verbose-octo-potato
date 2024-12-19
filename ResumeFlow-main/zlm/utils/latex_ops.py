import os
import jinja2
from zlm.utils.utils import write_file, save_latex_as_pdf

def escape_for_latex(data):
    if isinstance(data, dict):
        return {key: escape_for_latex(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [escape_for_latex(item) for item in data]
    elif isinstance(data, str):
        latex_special_chars = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\^{}",
            "\\": r"\textbackslash{}",
            "\n": "\\newline%\n",
            "-": r"{-}",
            "\xA0": "~",
            "[": r"{[}",
            "]": r"{]}",
        }
        return "".join([latex_special_chars.get(c, c) for c in data])
    return data

def latex_to_pdf(json_resume, dst_path):
    try:
        # Set up Jinja2 environment
        module_dir = os.path.dirname(__file__)
        templates_path = os.path.join(os.path.dirname(module_dir), "templates")
        latex_jinja_env = jinja2.Environment(
            block_start_string="\BLOCK{",
            block_end_string="}",
            variable_start_string="\VAR{",
            variable_end_string="}",
            comment_start_string="\#{",
            comment_end_string="}",
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(templates_path),
        )

        # Escape JSON data for LaTeX
        escaped_json_resume = escape_for_latex(json_resume)

        # Render LaTeX template
        resume_template = latex_jinja_env.get_template("resume.tex.jinja")
        resume_latex = resume_template.render(escaped_json_resume)

        # Write the rendered LaTeX to a temporary file
        tex_file_path = dst_path.replace(".pdf", ".tex")
        write_file(tex_file_path, resume_latex)

        # Convert LaTeX to PDF
        save_latex_as_pdf(tex_file_path, dst_path)
        return resume_latex
    except Exception as e:
        print(f"Error in latex_to_pdf: {e}")
        raise

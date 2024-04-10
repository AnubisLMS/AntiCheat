import sys
import json
import base64
from flask import Flask, render_template

app = Flask(__name__)
app.jinja_env.globals.update(b64=base64.urlsafe_b64encode)
data = None

def extract_ranges(overlapping_ranges, is_A):
    if is_A:
        return [{"start_pos": r["A_start_pos"], "end_pos": r["A_end_pos"]} for r in overlapping_ranges]
    else:
        return [{"start_pos": r["B_start_pos"], "end_pos": r["B_end_pos"]} for r in overlapping_ranges]

def code_to_highlighted_html(code, ranges):
    ranges.sort(key=lambda x: tuple(x["start_pos"]))
    in_range = False
    range_i = 0
    ln = 0
    col = 0

    html = ""

    for c in code:
        if not in_range:
            if range_i < len(ranges) and (ln, col) == tuple(ranges[range_i]["start_pos"]):
                html += "<span style='background-color: red; color: white'>"
                in_range = True
                # print((ln, col), range_i, in_range)
        else:
            if (ln, col) == tuple(ranges[range_i]["end_pos"]):
                html += "</span>"
                in_range = False
                range_i += 1
                # print((ln, col), range_i, in_range)

                # TODO: Need to figure out why subtrees of a subtree would be included in overlapping ranges
                while (range_i < len(ranges) and tuple(ranges[range_i]["start_pos"]) < (ln, col)):
                    range_i += 1

                if range_i < len(ranges) and (ln, col) == tuple(ranges[range_i]["start_pos"]):
                    html += "<span style='background-color: red; color: white'>"
                    in_range = True
                    # print((ln, col), range_i, in_range)

        html += c
        if c == '\n':
            ln += 1
            col = 0
        else:
            col += 1

    html += ""

    return html

@app.route("/")
def main():
    return render_template("main.html", data=data)

@app.route("/<int:index>")
def result(index):
    entry = data["result"][index - 1]

    with open(entry["submission_A"], 'r') as f:
        submission_A_code = f.read()
    with open(entry["submission_B"], 'r') as f:
        submission_B_code = f.read()

    return render_template(
        "result.html",
        entry=entry,
        submission_A_code=code_to_highlighted_html(
            submission_A_code,
            extract_ranges(entry["overlapping_ranges"], True)
        ),
        submission_B_code=code_to_highlighted_html(
            submission_B_code,
            extract_ranges(entry["overlapping_ranges"], False)
        ),
        prev=f"/{index - 1 if index > 1 else index}",
        next=f"/{index + 1 if index < len(data['result']) else index}"
    )

if __name__ == "__main__":
    data = json.loads(open(sys.argv[1]).read())
    data["result"].sort(key=lambda x: -x["similarity"])
    app.run(debug=True)

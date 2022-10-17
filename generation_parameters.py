import json
import re

re_param_code = r"\s*([\w ]+):\s*([^,]+)(?:,|$)"
re_param = re.compile(re_param_code)
re_params = re.compile(r"^(?:" + re_param_code + "){3,}$")
re_imagesize = re.compile(r"^(\d+)x(\d+)$")

def parse_generation_parameters(x: str):
    res = {}

    try:
        res = json.loads(x)
    except json.JSONDecodeError:
        res = {}

    if len(res) > 0:
        return res

    prompt = ""
    negative_prompt = ""

    done_with_prompt = False

    *lines, lastline = x.strip().split("\n")
    if not re_params.match(lastline):
        lines.append(lastline)
        lastline = ''

    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("Negative prompt:"):
            done_with_prompt = True
            line = line[16:].strip()

        if done_with_prompt:
            negative_prompt += ("" if negative_prompt == "" else "\n") + line
        else:
            prompt += ("" if prompt == "" else "\n") + line

    if len(prompt) > 0:
        res["Prompt"] = prompt

    if len(negative_prompt) > 0:
        res["Negative prompt"] = negative_prompt

    for k, v in re_param.findall(lastline):
        m = re_imagesize.match(v)
        if m is not None:
            res[k+"-1"] = m.group(1)
            res[k+"-2"] = m.group(2)
        else:
            res[k] = v

    return res

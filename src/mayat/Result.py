import json

def to_json(result_dict: dict) -> str:
    return json.dumps(result_dict, indent=4)

def to_text(result_dict: dict) -> str:
    result = ""

    result += str(result_dict["current_datetime"]) + "\n\n"

    result += f"Checking function: {result_dict['function']}" + "\n\n"

    result += "Warnings:" + "\n"
    for warning in result_dict["warnings"]:
        result += warning + "\n"
    result += "\n"

    result += f"Checker result:" + "\n"
    for entry in sorted(result_dict["result"], key=lambda x: x["similarity"], reverse=True):
        result += f"{entry['submission_A']} - {entry['submission_B']}:\t{entry['similarity']:%}" + "\n"
    result += "\n"

    result += f"{result_dict['execution_time']}s" + "\n"

    return result

# def print_str(result_dict: dict):
#     print(result_dict["current_datetime"])
#     print()

#     print(f"Checking function: {result_dict['function']}")
#     print()

#     print("Warnings:")
#     for warning in result_dict["warnings"]:
#         print(warning)
#     print()

#     print(f"Checker result:")
#     for entry in sorted(result_dict["result"], key=lambda x: x["similarity"], reverse=True):
#         print(f"{entry['submission_A']} - {entry['submission_B']}:\t{entry['similarity']:%}")
#     print()

#     print(f"{result_dict['execution_time']}s")

def serialize_result(result_dict: dict, format: str, list_all: bool) -> str:
    if not list_all:
        result_dict["result"] = list(
            filter(lambda x: x["similarity"] > 0, result_dict["result"])
        )

    if format == "JSON":
        return to_json(result_dict)
    else:
        result = to_text(result_dict)
        if format != "TXT":
            result = "Unknown output format. Using TXT format\n\n" + result
        return result

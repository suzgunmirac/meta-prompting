import os
import tempfile
from subprocess import Popen, PIPE, TimeoutExpired


# Python code execution function with timeout
# TODO: Improve the security of this function by using a sandboxed environment
def execute_code_with_timeout(code, timeout=3):
    with tempfile.NamedTemporaryFile(
        mode="w+t", suffix=".py", delete=False
    ) as temp_file:
        temp_file.write(code)
        temp_file.flush()

    try:
        # In case alias python=python3 is not set, use python3 instead of python
        process = Popen(["python3", temp_file.name], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate(timeout=timeout)
        captured_output = stdout.decode().strip()
        error_output = stderr.decode().strip()

        if captured_output == "":
            if error_output != "":
                captured_output = f"Error in execution: {error_output}"
            else:
                captured_output = "(No output was generated. It is possible that you did not include a print statement in your code.)"

    except TimeoutExpired:
        process.kill()
        captured_output = "Execution took too long, aborting..."

    finally:
        os.remove(temp_file.name)

    return captured_output

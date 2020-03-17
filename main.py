import subprocess
import os
import yaml
import argparse

def run(file_name, input_data=""):
    process = subprocess.run(['python3', file_name], input=input_data, text=True)
    return process.stdout

def generate_testcase(inputter_file_name, outputter_file_name):
    input_data = run(inputter_file_name)
    output_data = run(outputter_file_name, input_data)
    return input_data, output_data

def generate_batch(config, inputter_file_name, outputter_file_name):
    name = config['name']
    testcases_name = config['testcase']['name']
    num_testcases = config['testcase']['num']
    points = config['points']

    batch_dir = "testcase/{0}".format(name)
    os.mkdir(batch_dir)
    manifest = {'type': 'batch', 'name': name, 'metadata': {'points': points}}
    with open("{0}/manifest.yaml".format(batch_dir), "w") as manifest_file:
        yaml.dump(manifest, manifest_file)
    for testcase_num in range(num_testcases):
        input_data, output_data = generate_testcase()
        testcase_name = testcase_name.format(testcase_num+1)
        with open("{0}/{1}/{1}.in", "w").format(testcase_name) as testcase_input_file:
            testcase_input_file.write(input_data)
        with open("{0}/{1}/{1}.out", "w").format(testcase_name) as testcase_output_file:
            testcase_output_file.write(output_data)

def main(config):
    os.mkdir("testcases")
    inputter_file_name = config['generator']['input']
    outputter_file_name = config['generator']['output']
    batches = config['testcase']['batch']
    for batch in batches:
        generate_batch(batch, inputter_file_name, outputter_file_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate testdata in PNOJ format.')
    parser.add_argument('configuration', help='File name of the configuration YAML.')
    args = parser.parse_args()
    with open(args.configuration, "r") as config_file:
        config = yaml.safe_load(config_file)
    main(config)

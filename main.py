import subprocess
import os
import yaml
import argparse
import math

def run(file_name, input_data=""):
    process = subprocess.run(['python3', file_name], input=input_data, text=True, capture_output=True)
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
    testcase_num_digits = int(math.log10(num_testcases))+1

    batch_dir = "testcases/{0}".format(name)
    os.mkdir(batch_dir)
    manifest = {'type': 'batch', 'name': name, 'metadata': {'points': points}}
    with open("{0}/manifest.yaml".format(batch_dir), "w") as manifest_file:
        yaml.dump(manifest, manifest_file)
    for testcase_num in range(num_testcases):
        input_data, output_data = generate_testcase(inputter_file_name, outputter_file_name)
        testcase_name = testcases_name.format(str(testcase_num+1).zfill(testcase_num_digits))
        os.mkdir("{0}/{1}".format(batch_dir, testcase_name))
        with open("{0}/{1}/{1}.in".format(batch_dir, testcase_name), "w") as testcase_input_file:
            testcase_input_file.write(input_data)
        with open("{0}/{1}/{1}.out".format(batch_dir, testcase_name), "w") as testcase_output_file:
            testcase_output_file.write(output_data)

def main(config):
    inputter_file_name = config['generator']['input']
    outputter_file_name = config['generator']['output']
    batches = config['testcase']['batch']
    os.mkdir("testcases")
    for batch in batches:
        generate_batch(batch, inputter_file_name, outputter_file_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate testdata in PNOJ format.')
    parser.add_argument('configuration', help='File name of the configuration YAML.')
    args = parser.parse_args()
    with open(args.configuration, "r") as config_file:
        config = yaml.safe_load(config_file)
    main(config)

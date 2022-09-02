Instruction for installation

Step 1: Download and install Anaconda at https://www.anaconda.com/.

Step 2: Open your terminal (mac) or Anaconda Prompt (Windows), run the command
conda --version
to test the installation.

Step 3: Open your terminal or Anaconda Prompt, run the following commands to install Gurobi:
conda config --add channels https://conda.anaconda.org/gurobi
conda install gurobi

Step 4: Register the Gurobi academic license by your UMich email at
https://www.gurobi.com/downloads/end-user-license-agreement-academic/
After clicking "I Accept These Conditions", you will get a command line starting with "grbgetkey".

Step 5: Open your terminal or Anaconda Prompt, run the command line starting with "grbgetkey" to write the license.
For example: grbgetkey 0c1286d6-xxxx-xxxx-xxxx-...

Step 6: Open Anaconda Navigator, install and launch Spyder. Now you can write python code and use Gurobi to solve your model!


Instruction for running the code

Step 1: Ensure that you install Anaconda and Gurobi following the above instructions.

Step 2: Open Spyder and the code files. Select "Run" -> "Run" on the toolbar, you will get the results in the console.
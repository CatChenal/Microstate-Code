from pathlib import Path


def update_msa(output_dir: str = None):
    """Hack to download latest ms_analysis.py from github GunnerLab/Stable-MCCE repo
       as no updated conda package on channel 'newbooks' exists as of 12-10-2023.
       Note: To update `ms_analysis.py`: back it up or delete it, then rerun: `python update_msa.py`.
       Arg:
       output_dir (str): Folder where to save the downloaded module.
    """

    try:
        import ms_analysis as msa
        print("Import of ms_analysis was successful.",
              "If you meant to update it, remove or rename it, then run `python update_msa.py` again.",
              sep = "\n"
        )

    except ModuleNotFoundError:
        here = Path(__file__).parent

        if output_dir is None:
            output_path = here.joinpath("ms_analysis.py") #"./ms_analysis.py")
        else:
            output_path = Path(output_dir).joinpath("ms_analysis.py")

        if output_path.exists():
            print("Module already exists. Remove or rename, then run `python update_msa.py` again.")
            return

        latest_msa_url = "https://raw.githubusercontent.com/GunnerLab/Stable-MCCE/master/bin/ms_analysis.py"
        curl_cmd = f"curl {latest_msa_url} -o {str(output_path)}".split()

        import subprocess

        try:
            subprocess.run(curl_cmd, check=True)
        except subprocess.CalledProcessError as E:
            raise EnvironmentError(f"Could not download ms_analysis.py from 'GunnerLab/Stable-MCCE'.\n{E}")


if __name__ == "__main__":
    update_msa()

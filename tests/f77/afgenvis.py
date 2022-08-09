import argparse
import logging

import numpy as np
import pandas as pd
import plotnine as pn

log = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("afgen_file", metavar="afgen_file", type=str, help="afgen file")
    parser.add_argument("cp_file", metavar="cp_file", type=str, help="cp file")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s (%(levelname)s): %(message)s",
    )
    log.info(f"Reading AFGEN file: {args.afgen_file}")

    afoil = pd.read_csv(args.afgen_file, sep=",", names=["x", "z"], header=None)

    af_plt = (
        pn.ggplot(afoil, pn.aes("x", "z"))
        + pn.geom_point()
        + pn.geom_path()
        + pn.coord_fixed(xlim=(-1.25, 1.25), ylim=(-1, 1))
        + pn.scale_x_continuous(
            breaks=np.arange(-1, 1.5, 0.5),
            minor_breaks=np.arange(-1.25, 1.5, 0.25),
            expand=(0, 0),
        )
        + pn.scale_y_continuous(breaks=np.arange(-1, 1.25, 0.25), expand=(0, 0))
        + pn.theme_bw()
    )

    log.info(f"Reading CP file: {args.cp_file}")
    cp = pd.read_csv(args.cp_file, sep=",", names=["x", "cp"], header=None)

    cp_plt = (
        pn.ggplot(cp, pn.aes("x", "cp"))
        + pn.geom_point()
        + pn.geom_path()
        + pn.scale_x_continuous(
            breaks=np.linspace(-1, 1, 5),
            minor_breaks=np.arange(-1.25, 1.5, 0.25),
            expand=(0, 0),
        )
        + pn.theme_bw()
    )
    print(cp_plt)

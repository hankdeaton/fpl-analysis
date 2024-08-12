import pandas as pd
import numpy as np


def get_replacements(all_df):
    # Function to get the replacement level players theoretically left over

    # Roster size
    roster = ["G",
              "D", "D", "D",
              "M", "M", "M",
              "F", "F", "F",
              "G|D|M|F", "G|D|M|F", "G|D|M|F", "G|D|M|F", "G|D|M|F"]

    # remove all the starters
    for r in roster:
        first10 = all_df[all_df['Position'].str.contains(r)].index[0:10]  # Get the first 10 in the list (10 teams)

        # print(first12)

        all_df = all_df.drop(all_df.index[first10])  # remove the first 12
        all_df = all_df.reset_index(drop=True)

    return all_df


def calc_top_n(rep_df, N):
    # Function to calculate average of the top N players at each position

    # Sort by FP/G
    rep_df = rep_df.sort_values(by=['FPts'], ascending=False)

    ps = ["G", "D", "M", "F"]
    rpv = pd.DataFrame(columns=['Position', 'RPV'])
    for p in ps:
        rp = rep_df[rep_df['Position'].str.contains(p)][0:N]  # get the first five from the replacement player list
        rpv = rpv.append({'Position': p, 'RPV': np.mean(rp["FPts"])}, ignore_index=True)

    return rpv


def create_draft_rankings(fname):

    # read in the projections, sort by ADP
    proj_df = pd.read_csv(fname)

    # Replace the empty ADPs
    proj_df['ADP'].replace({'-': '1250'}, inplace=True)

    # Cahnge ADP column to float
    proj_df['ADP'] = proj_df.ADP.astype(float)

    # Sort in ascending order by ADP
    proj_df = proj_df.sort_values(by=['ADP'], ascending=True)

    # Calculate the replacement level player value
    reps_df = get_replacements(proj_df)

    # Calculate the average of the top 5 RP at each position
    rpv_df = calc_top_n(reps_df, 7)

    # Calculate estimated number of games
    proj_df["G"] = proj_df["FPts"] / proj_df["FP/G"]

    # calculate VORP/G
    proj_df["VORPpg"] = 0
    for index, row in rpv_df.iterrows():
        proj_df.loc[proj_df['Position'].str.contains(row["Position"]), ["VORPpg"]] = proj_df["FP/G"] - row[
            "RPV"]

    proj_df["VORP"] = proj_df["VORPpg"] * proj_df["G"]
    proj_df["aVORP"] = proj_df["VORP"] / 38

    proj_df = proj_df.sort_values(by=['aVORP'], ascending=False)

    return proj_df

from predict import preprocess
from argparse import ArgumentParser


def add_negative_data(data):
    neg_data = data.copy()
    mask = data.columns.str.contains('ight')
    neg_data.loc[:, mask] = data.loc[:, mask].sample(frac=1, random_state=42)
    return data.append(neg_data).reset_index(drop=True)


def main():
    argparser = ArgumentParser()
    argparser.add_argument('--infile', dest='infile', required=True)
    argparser.add_argument('--out', '-o', dest='out', required=True)
    args = argparser.parse_args()

    data = preprocess(args.infile)
    data = add_negative_data(data)
    data.to_csv(args.out, index=False, compression='zip')

    return data


if __name__ == '__main__':
    main()

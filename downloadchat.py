import os
import time


# twitch-chatlog by freaktechnik: https://github.com/freaktechnik/twitch-chatlog
# pip install twitch-chatlog


def readVods(filename):
    vodids = list()
    with open(filename, 'r') as f:
        for line in f:
            vodids.append(line.strip().split(',')[0])
        if not vodids[0].isnumeric():
            vodids = vodids[1:]  # cuts out headers if any
    return vodids


def downloadchat(vodid, outpath, faileddownloads):
    outfile = os.path.join(outpath, f'{vodid}chatlog.txt').replace('\\', '/')
    commands = f'twitch-chatlog {vodid} -l 0 > {outfile}'
    print(commands)

    out = os.popen(commands).read()
    if 'FetchError' in out:
        print(f'Error in downloading vod {vodid}')
        faileddownloads += f'{vodid}\n'
    elif 'RequestError' in out:
        print(f'Error in downloading vod {vodid}')
        faileddownloads += f'{vodid}\n'
    else:
        print(f'VOD {vodid} Downloaded')


if __name__ == '__main__':
    relpath = os.path.dirname(__file__)
    # change to downloaderrors.csv after first run to retry failed attempts
    vodfile = os.path.join(relpath, 'data', 'vodinfos.csv')
    vodids = readVods(vodfile)
    outpath = os.path.join(relpath, 'data')
    faileddownloads = ''
    for vod in vodids:
        downloadchat(vod, outpath, faileddownloads)
        time.sleep(90)  # mitigates rate limit
    if faileddownloads != '':
        errorfile = os.path.join(relpath, 'data', 'downloaderrors.csv')
        with open(errorfile, 'w+'):
            errorfile.write(faileddownloads)

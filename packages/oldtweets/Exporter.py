# -*- coding: utf-8 -*-
import sys, getopt
if sys.version_info[0] < 3:
    import packages.oldtweets.got
else:
    import packages.oldtweets.got3 as got

def main(argv):
    tweetList = []

    if len(argv) == 0:
        print('You must pass some parameters. Use \"-h\" to help.')
        return

    if len(argv) == 1 and argv[0] == '-h':
        f = open('exporter_help_text.txt', 'r')
        print(f.read())
        f.close()

        return

    try:
        opts, args = getopt.getopt(argv.split(), "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))
        tweetCriteria = got.manager.TweetCriteria()

        for opt,arg in opts:
            if opt == '--username':
                tweetCriteria.username = arg

            elif opt == '--since':
                tweetCriteria.since = arg

            elif opt == '--until':
                tweetCriteria.until = arg

            elif opt == '--querysearch':
                tweetCriteria.querySearch = arg

            elif opt == '--toptweets':
                tweetCriteria.topTweets = True

            elif opt == '--maxtweets':
                tweetCriteria.maxTweets = int(arg)

            elif opt == '--near':
                tweetCriteria.near = '"' + arg + '"'

            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--output':
                outputFileName = arg

        #outputFile = codecs.open(outputFileName, "w+", "utf-8")
        #outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

        print('Searching...\n')

        def receiveBuffer(tweets):
            return
            #tweetList.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
            #outputFile.flush();
            #print('More %d saved on file...\n' % len(tweets))

        totalTweets = got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
        for t in totalTweets:
            data = {}
            data['user'] = {}
            data['user']['screen_name'] = t.username

            # Not available - Hardcode to default
            data['user']['created_at'] = 'Sun Jan 01 01:01:01 +0000 2017'
            data['user']['followers_count'] = -1
            data['user']['utc_offset'] = 0

            data['text'] = t.text
            data['retweet_count'] = t.retweets
            data['id_str'] = t.id
            data['created_at'] = t.formatted_date

            tweetList.append(data)

    except arg:
        print('Arguments parser error, try -h' + arg)
    finally:
        return tweetList

if __name__ == '__main__':
    main(sys.argv[1:])

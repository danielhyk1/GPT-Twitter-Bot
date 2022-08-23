import http.server
import http.client
import urllib.parse
import ast
import tweepy

class TwitterHandler( http.server.SimpleHTTPRequestHandler):

    def session_store( self, token ):
        self.send_header( 'Set-Cookie', 'auth={};'.format( token ) )

    def session_retrieve( self ):
        if not self.headers.get( 'Cookie' ):
            raise Exception( 'No session cookie available.' )
        
        # bit ugly, but gets token stored as dictionary from cookie
        try:
            return ast.literal_eval( self.headers.get( 'Cookie' ).split( '=' )[ 1 ] )
        except:
            # just returns it as a string
            return self.headers.get( 'Cookie' ).split( '=' )[ 1 ]

    def do_GET( self ):
        #REPLACE TOKENS BELOW TO AUTHENTICATE TO YOUR OWN BOT
        auth = tweepy.OAuthHandler('w8Eab6JPxsWnEXe52GNmjwyc6', '6qG541Hymq05uk12tdD9E6u0RzMs9FF7962cqxaiJHnuM5YliZ')
        req = urllib.parse.urlparse( 'http://localhost:8080' + self.path )
        #verifier = request.GET.get('oauth_verifier')
        try:
            #auth.get_access_token(verifier)
            redirect_link = auth.get_authorization_url()
            #print(redirect_link)
        except tweepy.TweepError:
            print('ERROR')
        # return requests from Twitter go through this branch
        if req.query:
            token = self.session_retrieve()
            res = req.query.partition('verifier=')[2]
            #print('verifier')
            #print(res)
            auth.request_token = {'oauth_token': token, 'oauth_token_secret': res}
            access_token = auth.get_access_token(res)
                                   # TODO: replace the 'XXXXX' with the access token and  secret returned from Twitter.
            print( "Access Token: {}\nAccess Token Secret: {}".format(access_token[0], access_token[1]))
            exit()

        # initial requests (before the redirect to Twitter) go through this branch
        else:

            # TODO: replace the 'XXXXX' placeholders with the redirect url and request token
            self.send_response( 307 )
            self.send_header('Location', redirect_link)
            #print(auth.request_token['oauth_token'])
            #print(auth.request_token['oauth_token_secret'])
            self.session_store(auth.request_token['oauth_token'])
            self.end_headers()


def run( server_class = http.server.HTTPServer, handler_class = TwitterHandler ):
    server_address = ('localhost', 8080)
    httpd = server_class( server_address, handler_class )
    httpd.serve_forever()
    do_GET(self)

if __name__ == '__main__':
    run()

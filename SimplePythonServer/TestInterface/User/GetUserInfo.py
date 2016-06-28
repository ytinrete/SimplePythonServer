'''
this is the class testing the server handling request in path /Interface/User/GetUserInfo
the request path should be like this: http://localhost:9000/Interface/User/GetUserInfo
'''


class GetUserInfo:
    get_handle_count = 0
    post_handle_count = 0

    def do_GET(self, queries):
        print('solving GET in GetUserInfo')
        print('the queries are:', queries)
        if queries:
            response = 'GetUserInfo got:{'
            for k in queries:
                response += k + ':['
                # got list in dict
                for v in queries[k]:
                    response += v + '-'
                response += '], '
            response += '}\n'
        else:
            response = 'GetUserInfo got nothing in queries\n'
        GetUserInfo.get_handle_count += 1
        response += 'handle GET finish! times:' + str(GetUserInfo.get_handle_count)
        print('response:\n' + response)
        # note that you must return with bytes data
        return bytes(response, 'utf-8')

    def do_POST(self, req_content, queries):
        print('solving POST in GetUserInfo')
        print('the queries are:', queries)
        if queries:
            response = 'GetUserInfo got:{'
            for k in queries:
                response += k + ':['
                # got list in dict
                for v in queries[k]:
                    response += v + '-'
                response += '], '
            response += '}\n'
        else:
            response = 'TestRootClass got nothing in queries\n'
        response += 'here is the post body:' + req_content + '\n'
        GetUserInfo.post_handle_count += 1
        response += 'handle POST finish! times:' + str(GetUserInfo.post_handle_count)
        print('response:\n' + response)
        # note that you must return with bytes data
        return bytes(response, 'utf-8')

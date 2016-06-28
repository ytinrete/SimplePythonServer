'''
this is the class testing the server handling request in root path
the request path should be like this: http://localhost:9000/TestRootClass
'''


class TestRootClass:
    get_handle_count = 0
    post_handle_count = 0

    def do_GET(self, queries):
        print('solving GET in TestRootClass')
        print('the queries are:', queries)
        if queries:
            response = 'TestRootClass got:{'
            for k in queries:
                response += k + ':['
                # got list in dict
                for v in queries[k]:
                    response += v + '-'
                response += '], '
            response += '}\n'
        else:
            response = 'TestRootClass got nothing in queries\n'
        TestRootClass.get_handle_count += 1
        response += 'handle GET finish! times:' + str(TestRootClass.get_handle_count)
        print('response:\n' + response)
        # note that you must return with bytes data
        return bytes(response, 'utf-8')

    def do_POST(self, req_content, queries):
        print('solving POST in TestRootClass')
        print('the queries are:', queries)
        if queries:
            response = 'TestRootClass got:{'
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
        TestRootClass.post_handle_count += 1
        response += 'handle POST finish! times:' + str(TestRootClass.post_handle_count)
        print('response:\n' + response)
        # note that you must return with bytes data
        return bytes(response, 'utf-8')

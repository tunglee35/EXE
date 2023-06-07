import 'package:http/http.dart' as http;
import 'dart:math';
import 'dart:convert';
import 'dart:async';
import 'dart:io';
import 'package:meta/meta.dart';
import 'dart:io';

const String BARD_COOKIE =
    "XQh4bKIq8HK-lA5_SB7kikDJgCTziUz4pASEJ0y7dnp30YTr1oMJ2esSjRCv4XiAcv5IcQ.";

const String baseURL = "bard.google.com";

const SESSION_HEADERS = {
  "Host": baseURL,
  "X-Same-Domain": "1",
  "User-Agent":
      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
  "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
  "Origin": "https://bard.google.com",
  "Referer": "https://bard.google.com/",
  "Timeout": "20",
  "Cookie": "__Secure-1PSID=$BARD_COOKIE",
};

String endPoint(String endPoint) => "$baseURL/$endPoint";

Map<String, String> headerBearerOption(String token) => {
      "Content-Type": "application/json",
      'Authorization': 'Bearer $token',
    };

enum ApiState { loading, success, error, notFound }

class Bard {
  final token = BARD_COOKIE;
  final timeout = 20;
  final proxies = {};
  final session = http.Client();
  final language = 'en';
  final runCode = false;
  late String conversationId = '';
  late String responseId = '';
  late String choiceId = '';
  late num reqId = 0;
  late String SNlM0e = '';

  Bard() {
    var random = Random();
    var digits = '0123456789';
    var code = int.parse(String.fromCharCodes(Iterable.generate(
        4, (_) => digits.codeUnitAt(random.nextInt(digits.length)))));
    reqId = code;
  }

  Future<Map<String, dynamic>> getAnswer(String inputText) async {
    final params = {
      'bl': 'boqassistant-bard-web-server20230419.00p1',
      'reqid': reqId.toString(),
      'rt': 'c',
    };

    // Make post data structure and insert prompt
    final inputTextStruct = [
      [inputText],
      null,
      [conversationId, responseId, choiceId],
    ];

    if (SNlM0e.isEmpty) {
      setSnim0e();
    }
    final data = {
      'f.req': jsonEncode([null, jsonEncode(inputTextStruct)]),
      'at': SNlM0e,
    };

    // Get response
    final uri = Uri.new(
      scheme: 'https',
      host: baseURL,
      path:
          '/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate',
      queryParameters: params,
    );

    final response = await session.post(
      uri,
      body: data,
      headers: SESSION_HEADERS,
    );

    // Post-processing of response
    final respDict = json.decode(response.body.split('\n')[3])[0][2];

    if (respDict == null) {
      return {'content': 'Response Error: ${response.body}.'};
    }

    final parsedAnswer = json.decode(respDict);

    // Gather image links
    final images = <String>{};
    if (parsedAnswer.length >= 3) {
      if (parsedAnswer[4][0].length >= 4 && parsedAnswer[4][0][4] != null) {
        for (final img in parsedAnswer[4][0][4]) {
          try {
            images.add(img[0][0][0]);
          } catch (e) {
            // pass
          }
        }
      }
    }

    // Get code
    String code;
    try {
      code = parsedAnswer[0][0].split('```')[1].substring(6);
    } catch (e) {
      code = '';
    }

    // Return dictionary object
    final bardAnswer = {
      'content': parsedAnswer[0][0],
      'conversation_id': parsedAnswer[1][0],
      'response_id': parsedAnswer[1][1],
      'factualityQueries': parsedAnswer[3],
      'textQuery': parsedAnswer[2].isNotEmpty ? parsedAnswer[2][0] : '',
      'choices': [
        for (final x in parsedAnswer[4]) {'id': x[0], 'content': x[1]}
      ],
      'links': extractLinks(parsedAnswer[4]),
      'images': images,
      'code': code,
    };
    conversationId = bardAnswer['conversation_id'];
    responseId = bardAnswer['response_id'];
    choiceId = bardAnswer['choices'][0]['id'];
    reqId += 100000;

    return bardAnswer;
  }

  Future<String> setSnim0e() async {
    if (!token.endsWith('.')) {
      throw Exception(
        '__Secure-1PSID value must end with a single dot. Enter correct __Secure-1PSID value.',
      );
    }

    final uri = Uri(
      scheme: 'https',
      host: baseURL,
    );
    final value = await session.get(uri, headers: SESSION_HEADERS);

    if (value.statusCode != HttpStatus.ok) {
      throw Exception(
        'Response code not 200. Response Status is ${value.statusCode}',
      );
    }

    var snim0e = RegExp(r'SNlM0e":"(.*?)"').firstMatch(value.body)?.group(1);
    if (snim0e == null) {
      throw Exception(
          'SNlM0e value not found in response. Check __Secure-1PSID value.');
    }

    print('set snim0e: $snim0e');
    SNlM0e = snim0e;
    return snim0e;
  }

  List<String> extractLinks(List<dynamic> data) {
    List<String> links = [];
    for (var item in data) {
      if (item is List) {
        links.addAll(extractLinks(item));
      } else if (item is String &&
          item.startsWith('http') &&
          !item.contains('favicon')) {
        links.add(item);
      }
    }
    return links;
  }
}

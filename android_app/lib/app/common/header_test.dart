import 'package:test/test.dart';
import './headers.dart';
import 'dart:io';

void main() {
  var bard = Bard();
  var resp = '';

  group('get_snim0e', () {
    test('it works', () async {
      resp = await bard.setSnim0e();
      expect(resp, isNotEmpty);
    });
  });

  group('get answer', () {
    test('it works', () async {
      var query = 'how to build a website?';
      var resp = await bard.getAnswer(query);

      expect(resp['content'], isNotEmpty);
      print('Answer is ${resp['content']}');
    });
  });
}

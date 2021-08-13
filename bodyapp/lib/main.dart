import 'package:flutter/material.dart';
import 'package:pixel_perfect/pixel_perfect.dart';

import 'home/home.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: PixelPerfect(
        assetPath: 'design/screens/home.png',
        scale: .64,
        initOpacity: 0.5,
        child: HomeScreen(),
      ),
    );
  }
}

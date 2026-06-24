<!-- # Laravel Mix -->
# Laravel Mix

- [Introduction](#introduction)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Mix](https://github.com/laravel-mix/laravel-mix), a package developed by [Laracasts](https://laracasts.com) creator Jeffrey Way, provides a fluent API for defining [webpack](https://webpack.js.org) build steps for your Laravel application using several common CSS and JavaScript pre-processors. -->
[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com)의 창립자인 Jeffrey Way가 개발한 패키지로, Laravel 애플리케이션에서 자주 사용하는 CSS 및 JavaScript 전처리기를 활용하여 [webpack](https://webpack.js.org) 빌드 단계를 손쉽게 정의할 수 있는 직관적인 API를 제공합니다.

<!-- In other words, Mix makes it a cinch to compile and minify your application's CSS and JavaScript files. Through simple method chaining, you can fluently define your asset pipeline. For example: -->
즉, Mix를 사용하면 애플리케이션의 CSS와 JavaScript 파일을 쉽게 컴파일하고, 파일 크기를 줄여서 배포용으로 최적화할 수 있습니다. 메서드 체이닝 방식으로 에셋(정적 파일) 처리 파이프라인을 매우 간단하게 구성할 수 있습니다. 예를 들어,

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

<!-- If you've ever been confused and overwhelmed about getting started with webpack and asset compilation, you will love Laravel Mix. However, you are not required to use it while developing your application; you are free to use any asset pipeline tool you wish, or even none at all. -->
만약 webpack과 에셋 컴파일 환경 구축이 어렵거나 복잡하다고 느꼈다면, Laravel Mix가 큰 도움이 될 것입니다. 그러나 Mix를 반드시 사용해야 하는 것은 아니며, 원하는 다른 에셋 파이프라인 도구를 사용하거나 아예 별도의 처리를 하지 않아도 무방합니다.

> [!NOTE]
> Vite가 새로운 Laravel 설치 시 Laravel Mix를 대체하였습니다. Mix에 대한 자세한 문서는 [official Laravel Mix](https://laravel-mix.com/) 웹사이트에서 확인하실 수 있습니다. Vite로 전환하고 싶으시다면 [Vite migration guide](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고해 주세요.
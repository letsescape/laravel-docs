<!-- # Laravel Mix -->
# Laravel Mix

- [Introduction](#introduction)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Mix](https://github.com/laravel-mix/laravel-mix), a package developed by [Laracasts](https://laracasts.com) creator Jeffrey Way, provides a fluent API for defining [webpack](https://webpack.js.org) build steps for your Laravel application using several common CSS and JavaScript pre-processors. -->
[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com)의 창립자인 Jeffrey Way가 개발한 패키지로, [webpack](https://webpack.js.org)과 함께 사용할 때 Laravel 애플리케이션의 빌드 과정을 간결하게 정의할 수 있는 직관적인 API를 제공합니다. 이로써 다양한 CSS 및 JavaScript 전처리기를 쉽게 사용할 수 있습니다.

<!-- In other words, Mix makes it a cinch to compile and minify your application's CSS and JavaScript files. Through simple method chaining, you can fluently define your asset pipeline. For example: -->
즉, Mix를 이용하면 애플리케이션의 CSS와 JavaScript 파일을 간단하게 컴파일하고, 압축할 수 있습니다. 메서드 체이닝 방식으로 명확하게 자산 파이프라인을 구성할 수 있습니다. 예를 들어 다음과 같이 사용할 수 있습니다.

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

<!-- If you've ever been confused and overwhelmed about getting started with webpack and asset compilation, you will love Laravel Mix. However, you are not required to use it while developing your application; you are free to use any asset pipeline tool you wish, or even none at all. -->
webpack과 자산 컴파일에 처음 입문하거나 혼란스러웠던 경험이 있다면, Laravel Mix는 분명 큰 도움이 될 것입니다. 하지만, 애플리케이션을 개발할 때 반드시 Mix를 사용해야 하는 것은 아니며, 원하는 다른 자산 파이프라인 도구를 자유롭게 사용할 수 있고, 아예 특정 도구를 사용하지 않아도 괜찮습니다.

> [!NOTE]
> 현재는 새로운 Laravel 설치 시 Vite가 Laravel Mix를 대체하였습니다. Mix 관련 공식 문서는 [official Laravel Mix](https://laravel-mix.com/)에서 확인할 수 있습니다. 만약 Vite로 전환하고 싶다면, [Vite migration guide](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하시기 바랍니다.

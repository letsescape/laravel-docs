<!-- # Compiling Assets (Mix) -->
# Compiling Assets (Mix)

- [Introduction](#introduction)
- [Installation & Setup](#installation)
- [Running Mix](#running-mix)
- [Working With Stylesheets](#working-with-stylesheets)
    - [Tailwind CSS](#tailwindcss)
    - [PostCSS](#postcss)
    - [Sass](#sass)
    - [URL Processing](#url-processing)
    - [Source Maps](#css-source-maps)
- [Working With JavaScript](#working-with-scripts)
    - [Vue](#vue)
    - [React](#react)
    - [Vendor Extraction](#vendor-extraction)
    - [Custom Webpack Configuration](#custom-webpack-configuration)
- [Versioning / Cache Busting](#versioning-and-cache-busting)
- [Browsersync Reloading](#browsersync-reloading)
- [Environment Variables](#environment-variables)
- [Notifications](#notifications)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Mix](https://github.com/JeffreyWay/laravel-mix), a package developed by [Laracasts](https://laracasts.com) creator Jeffrey Way, provides a fluent API for defining [webpack](https://webpack.js.org) build steps for your Laravel application using several common CSS and JavaScript pre-processors. -->
[Laravel Mix](https://github.com/JeffreyWay/laravel-mix)는 [Laracasts](https://laracasts.com)의 창립자인 Jeffrey Way가 개발한 패키지로, Laravel 애플리케이션을 위한 [webpack](https://webpack.js.org) 빌드 작업을 여러 가지 대표적인 CSS 및 JavaScript 전처리기를 사용하여 쉽게 정의할 수 있도록 유연한 API를 제공합니다.

<!-- In other words, Mix makes it a cinch to compile and minify your application's CSS and JavaScript files. Through simple method chaining, you can fluently define your asset pipeline. For example: -->
즉, Mix를 활용하면 애플리케이션의 CSS와 JavaScript 파일을 쉽고 빠르게 컴파일하고, 최소화할 수 있습니다. 단순한 메서드 체이닝 방식으로 자산 빌드 파이프라인을 명확하게 정의할 수 있습니다. 예를 들어:

```
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

<!-- If you've ever been confused and overwhelmed about getting started with webpack and asset compilation, you will love Laravel Mix. However, you are not required to use it while developing your application; you are free to use any asset pipeline tool you wish, or even none at all. -->
만약 webpack과 에셋 컴파일 환경을 처음 시작할 때 막막하거나 어렵게 느껴지셨다면, Laravel Mix를 정말 반길 것입니다. 다만, Mix 사용은 필수가 아니며, 개발 시 본인에게 맞는 어떤 에셋 파이프라인 도구든 자유롭게 사용할 수 있습니다. 혹은 아예 아무런 빌드 툴도 쓰지 않아도 됩니다.

> [!TIP]
> Laravel과 [Tailwind CSS](https://tailwindcss.com)로 애플리케이션을 빠르게 시작하고 싶다면, [application starter kits](/docs/8.x/starter-kits)를 참고해 보시기 바랍니다.

<a name="installation"></a>
<!-- ## Installation & Setup -->
## Installation & Setup

<a name="installing-node"></a>
<!-- #### Installing Node -->
#### Installing Node

<!-- Before running Mix, you must first ensure that Node.js and NPM are installed on your machine: -->
Mix를 실행하기 전에 먼저, Node.js와 NPM이 시스템에 설치되어 있어야 합니다:

```
node -v
npm -v
```

<!-- You can easily install the latest version of Node and NPM using simple graphical installers from [the official Node website](https://nodejs.org/en/download/). Or, if you are using [Laravel Sail](/docs/8.x/sail), you may invoke Node and NPM through Sail: -->
가장 간단하게는 [the official Node website](https://nodejs.org/en/download/)에서 그래픽 설치 프로그램을 받아 최신 버전의 Node와 NPM을 설치할 수 있습니다. 또는 [Laravel Sail](/docs/8.x/sail)을 사용하는 경우 Sail을 통해 Node와 NPM에 접근할 수도 있습니다:

```
./sail node -v
./sail npm -v
```

<a name="installing-laravel-mix"></a>
<!-- #### Installing Laravel Mix -->
#### Installing Laravel Mix

<!-- The only remaining step is to install Laravel Mix. Within a fresh installation of Laravel, you'll find a `package.json` file in the root of your directory structure. The default `package.json` file already includes everything you need to get started using Laravel Mix. Think of this file like your `composer.json` file, except it defines Node dependencies instead of PHP dependencies. You may install the dependencies it references by running: -->
이제 남은 작업은 Laravel Mix를 설치하는 것뿐입니다. Laravel을 새로 설치하면, 디렉터리 구조의 루트에 이미 `package.json` 파일이 포함되어 있습니다. 기본 `package.json`엔 Laravel Mix를 사용하기 위한 모든 의존성이 미리 포함되어 있습니다. 이 파일은 마치 `composer.json`과 비슷하게, PHP 의존성 대신 Node 의존성을 정의합니다. 다음 명령어로 의존성 설치를 시작할 수 있습니다:

```
npm install
```

<a name="running-mix"></a>
<!-- ## Running Mix -->
## Running Mix

<!-- Mix is a configuration layer on top of [webpack](https://webpack.js.org), so to run your Mix tasks you only need to execute one of the NPM scripts that are included in the default Laravel `package.json` file. When you run the `dev` or `production` scripts, all of your application's CSS and JavaScript assets will be compiled and placed in your application's `public` directory: -->
Mix는 [webpack](https://webpack.js.org) 위에서 작동하는 구성 레이어이므로, 기본 Laravel `package.json`에 포함된 NPM 스크립트 중 하나만 실행하면 Mix 태스크를 바로 사용할 수 있습니다. `dev` 또는 `production` 스크립트를 실행하면, 모든 CSS와 JavaScript 에셋이 컴파일되어 애플리케이션의 `public` 디렉터리에 저장됩니다:

```
// Run all Mix tasks...
npm run dev

// Run all Mix tasks and minify output...
npm run prod
```

<a name="watching-assets-for-changes"></a>
<!-- #### Watching Assets For Changes -->
#### Watching Assets For Changes

<!-- The `npm run watch` command will continue running in your terminal and watch all relevant CSS and JavaScript files for changes. Webpack will automatically recompile your assets when it detects a change to one of these files: -->
`npm run watch` 명령어는 터미널에서 계속 실행되며, 관련된 CSS와 JavaScript 파일의 변경사항을 모니터링합니다. webpack이 이 파일들 중 하나가 변경되는 것을 감지하면 에셋을 자동으로 다시 컴파일합니다:

```
npm run watch
```

<!-- Webpack may not be able to detect your file changes in certain local development environments. If this is the case on your system, consider using the `watch-poll` command: -->
특정 로컬 개발 환경에서는 webpack이 파일 변경을 감지하지 못할 수도 있습니다. 이 경우에는 `watch-poll` 명령어를 사용하는 것을 고려해 보십시오:

```
npm run watch-poll
```

<a name="working-with-stylesheets"></a>
<!-- ## Working With Stylesheets -->
## Working With Stylesheets

<!-- Your application's `webpack.mix.js` file is your entry point for all asset compilation. Think of it as a light configuration wrapper around [webpack](https://webpack.js.org). Mix tasks can be chained together to define exactly how your assets should be compiled. -->
애플리케이션의 `webpack.mix.js` 파일이 바로 에셋 컴파일의 진입점입니다. 이 파일은 [webpack](https://webpack.js.org)을 가볍게 감싼 설정 파일로 생각하시면 됩니다. Mix 태스크들은 메서드 체이닝 방식으로 연결할 수 있어, 에셋을 어떻게 컴파일할지 명확하게 정의할 수 있습니다.

<a name="tailwindcss"></a>
<!-- ### Tailwind CSS -->
### Tailwind CSS

<!-- [Tailwind CSS](https://tailwindcss.com) is a modern, utility-first framework for building amazing sites without ever leaving your HTML. Let's dig into how to start using it in a Laravel project with Laravel Mix. First, we should install Tailwind using NPM and generate our Tailwind configuration file: -->
[Tailwind CSS](https://tailwindcss.com)는 현대적인 유틸리티 우선 프레임워크로, HTML에서 한눈에 볼 수 있는 멋진 웹사이트를 쉽게 만들 수 있습니다. Laravel 프로젝트에서 Laravel Mix와 함께 Tailwind를 사용하는 시작 방법을 알아보겠습니다. 먼저 NPM을 사용해 Tailwind를 설치하고, Tailwind 설정 파일을 생성해야 합니다:

```
npm install

npm install -D tailwindcss

npx tailwindcss init
```

<!-- The `init` command will generate a `tailwind.config.js` file. The `content` section of this file allows you to configure the paths to all of your HTML templates, JavaScript components, and any other source files that contain Tailwind class names so that any CSS classes that are not used within these files will be purged from your production CSS build: -->
`init` 명령어를 실행하면 `tailwind.config.js` 파일이 생성됩니다. 이 파일의 `content` 섹션에서 HTML 템플릿, JavaScript 컴포넌트 등 Tailwind 클래스명이 포함된 모든 소스 파일의 경로를 설정할 수 있습니다. 이를 바탕으로 실제로 사용하지 않는 CSS 클래스는 프로덕션 빌드에서 제거됩니다:

```js
content: [
    './storage/framework/views/*.php',
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './resources/**/*.vue',
],
```

<!-- Next, you should add each of Tailwind's "layers" to your application's `resources/css/app.css` file: -->
이제 Tailwind의 각 "레이어"를 애플리케이션의 `resources/css/app.css` 파일에 추가해 주세요:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

<!-- Once you have configured Tailwind's layers, you are ready to update your application's `webpack.mix.js` file to compile your Tailwind powered CSS: -->
레이어 추가가 완료되면, 이제 `webpack.mix.js`를 수정해 Tailwind가 적용된 CSS를 컴파일할 수 있습니다:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css', [
        require('tailwindcss'),
    ]);
```

<!-- Finally, you should reference your stylesheet in your application's primary layout template. Many applications choose to store this template at `resources/views/layouts/app.blade.php`. In addition, ensure you add the responsive viewport `meta` tag if it's not already present: -->
마지막으로, 반드시 애플리케이션의 주요 레이아웃 템플릿(예: `resources/views/layouts/app.blade.php`)에서 이 스타일시트를 참조해야 합니다. 또한, 반응형 뷰포트(`meta` 태그)가 아직 없다면 추가하는 것도 잊지 마십시오:

```html
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href="/css/app.css" rel="stylesheet">
</head>
```

<a name="postcss"></a>
<!-- ### PostCSS -->
### PostCSS

<!-- [PostCSS](https://postcss.org/), a powerful tool for transforming your CSS, is included with Laravel Mix out of the box. By default, Mix leverages the popular [Autoprefixer](https://github.com/postcss/autoprefixer) plugin to automatically apply all necessary CSS3 vendor prefixes. However, you're free to add any additional plugins that are appropriate for your application. -->
[PostCSS](https://postcss.org/)는 CSS를 변환하기 위한 강력한 도구로, Laravel Mix에는 기본적으로 포함되어 있습니다. Mix는 대표적인 [Autoprefixer](https://github.com/postcss/autoprefixer) 플러그인을 사용해 필요한 CSS3 벤더 프리픽스를 자동으로 적용합니다. 필요하다면, 프로젝트에 맞는 어떤 추가 플러그인이든 자유롭게 사용할 수 있습니다.

<!-- First, install the desired plugin through NPM and include it in your array of plugins when calling Mix's `postCss` method. The `postCss` method accepts the path to your CSS file as its first argument and the directory where the compiled file should be placed as its second argument: -->
필요한 플러그인을 NPM으로 설치하고, Mix의 `postCss` 메서드를 호출할 때 해당 플러그인을 plugins 배열에 포함해 주세요. `postCss`의 첫 번째 인수는 CSS 파일 경로이며, 두 번째 인수는 컴파일된 파일이 생성될 디렉터리입니다:

```
mix.postCss('resources/css/app.css', 'public/css', [
    require('postcss-custom-properties')
]);
```

<!-- Or, you may execute `postCss` with no additional plugins in order to achieve simple CSS compilation and minification: -->
혹은, 추가 플러그인 없이 `postCss`를 실행하여 간단히 CSS를 컴파일하고 최소화할 수도 있습니다:

```
mix.postCss('resources/css/app.css', 'public/css');
```

<a name="sass"></a>
<!-- ### Sass -->
### Sass

<!-- The `sass` method allows you to compile [Sass](https://sass-lang.com/) into CSS that can be understood by web browsers. The `sass` method accepts the path to your Sass file as its first argument and the directory where the compiled file should be placed as its second argument: -->
`sass` 메서드를 이용하면 [Sass](https://sass-lang.com/) 파일을 웹 브라우저가 인식 가능한 CSS로 컴파일할 수 있습니다. `sass` 메서드의 첫 번째 인수는 Sass 파일 경로이고, 두 번째 인수는 컴파일된 CSS 파일이 기록될 디렉터리입니다:

```
mix.sass('resources/sass/app.scss', 'public/css');
```

<!-- You may compile multiple Sass files into their own respective CSS files and even customize the output directory of the resulting CSS by calling the `sass` method multiple times: -->
여러 개의 Sass 파일을 각각의 CSS 파일로 컴파일하거나, 결과 CSS의 출력 폴더를 직접 지정할 수도 있습니다. 이때는 `sass` 메서드를 여러 번 호출하면 됩니다:

```
mix.sass('resources/sass/app.sass', 'public/css')
    .sass('resources/sass/admin.sass', 'public/css/admin');
```

<a name="url-processing"></a>
<!-- ### URL Processing -->
### URL Processing

<!-- Because Laravel Mix is built on top of webpack, it's important to understand a few webpack concepts. For CSS compilation, webpack will rewrite and optimize any `url()` calls within your stylesheets. While this might initially sound strange, it's an incredibly powerful piece of functionality. Imagine that we want to compile Sass that includes a relative URL to an image: -->
Laravel Mix는 webpack 위에서 동작하므로, 몇 가지 webpack의 개념을 이해하면 좋습니다. CSS 컴파일 과정에서 webpack은 스타일시트 내의 모든 `url()` 호출을 자동으로 재작성하고 최적화합니다. 이 기능은 약간 낯설게 느껴질 수 있지만, 실제로 매우 강력합니다. 예를 들어, Sass에 상대 경로로 이미지를 추가한다고 가정해봅니다:

```
.example {
    background: url('../images/example.png');
}
```

> [!NOTE]
> 절대경로로 지정된 `url()`은 URL 재작성 대상에서 제외됩니다. 예를 들어, `url('/images/thing.png')` 또는 `url('http://example.com/images/thing.png')`와 같은 형태는 수정되지 않습니다.

<!-- By default, Laravel Mix and webpack will find `example.png`, copy it to your `public/images` folder, and then rewrite the `url()` within your generated stylesheet. As such, your compiled CSS will be: -->
기본적으로 Laravel Mix와 webpack은 `example.png` 파일을 찾아 `public/images` 폴더로 복사한 다음, 생성된 스타일시트 내에서 `url()` 경로도 알맞게 재작성합니다. 예를 들어, 결과 CSS는 다음과 같이 나타납니다:

```
.example {
    background: url(/images/example.png?d41d8cd98f00b204e9800998ecf8427e);
}
```

<!-- As useful as this feature may be, your existing folder structure may already be configured in a way you like. If this is the case, you may disable `url()` rewriting like so: -->
이 기능이 편리할 수도 있지만, 이미 파일 폴더 구조가 알맞게 되어 있는 경우에는 불필요하게 느껴질 수 있습니다. 이럴 때는 아래와 같이 `url()` 재작성을 비활성화할 수 있습니다:

```
mix.sass('resources/sass/app.scss', 'public/css').options({
    processCssUrls: false
});
```

<!-- With this addition to your `webpack.mix.js` file, Mix will no longer match any `url()` or copy assets to your public directory. In other words, the compiled CSS will look just like how you originally typed it: -->
이렇게 `webpack.mix.js`에 옵션을 추가하면 Mix는 더 이상 `url()`을 매칭하거나 에셋을 public 디렉터리로 복사하지 않습니다. 즉, 컴파일된 CSS는 본래 입력한 대로 남아 있게 됩니다:

```
.example {
    background: url("../images/thing.png");
}
```

<a name="css-source-maps"></a>
<!-- ### Source Maps -->
### Source Maps

<!-- Though disabled by default, source maps may be activated by calling the `mix.sourceMaps()` method in your `webpack.mix.js` file. Though it comes with a compile/performance cost, this will provide extra debugging information to your browser's developer tools when using compiled assets: -->
기본적으로 비활성화되어 있지만, `webpack.mix.js`에서 `mix.sourceMaps()` 메서드를 호출하면 소스 맵을 활성화할 수 있습니다. 소스 맵이 켜지면 빌드 및 성능에 약간의 비용이 들 수 있지만, 컴파일된 에셋을 브라우저 개발자 도구에서 디버깅하기 매우 편리해집니다:

```
mix.js('resources/js/app.js', 'public/js')
    .sourceMaps();
```

<a name="style-of-source-mapping"></a>
<!-- #### Style Of Source Mapping -->
#### Style Of Source Mapping

<!-- Webpack offers a variety of [source mapping styles](https://webpack.js.org/configuration/devtool/#devtool). By default, Mix's source mapping style is set to `eval-source-map`, which provides a fast rebuild time. If you want to change the mapping style, you may do so using the `sourceMaps` method: -->
Webpack은 다양한 [source mapping styles](https://webpack.js.org/configuration/devtool/#devtool)을 지원합니다. 기본적으로 Mix는 `eval-source-map` 스타일을 사용해 빠른 재빌드를 제공합니다. 만약 소스 맵 스타일을 변경하고 싶다면, `sourceMaps` 메서드로 지정할 수 있습니다:

```
let productionSourceMaps = false;

mix.js('resources/js/app.js', 'public/js')
    .sourceMaps(productionSourceMaps, 'source-map');
```

<a name="working-with-scripts"></a>
<!-- ## Working With JavaScript -->
## Working With JavaScript

<!-- Mix provides several features to help you work with your JavaScript files, such as compiling modern ECMAScript, module bundling, minification, and concatenating plain JavaScript files. Even better, this all works seamlessly, without requiring an ounce of custom configuration: -->
Mix는 최신 ECMAScript 문법 지원, 모듈 번들링, 최소화, 순수 JavaScript 파일 병합 등 다양한 기능을 제공합니다. 이러한 기능들은 별도의 복잡한 설정 없이도 자연스럽게 동작합니다:

```
mix.js('resources/js/app.js', 'public/js');
```

<!-- With this single line of code, you may now take advantage of: -->
단 한 줄의 코드만으로도, 아래의 이점을 누릴 수 있습니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The latest EcmaScript syntax.
- Modules
- Minification for production environments.
-->
- 최신 EcmaScript 문법 지원
- 모듈 사용
- 프로덕션 환경에서의 자바스크립트 코드 최소화

<!-- </div> -->
</div>

<a name="vue"></a>
<!-- ### Vue -->
### Vue

<!-- Mix will automatically install the Babel plugins necessary for Vue single-file component compilation support when using the `vue` method. No further configuration is required: -->
`vue` 메서드를 사용할 경우, Mix는 Vue 싱글 파일 컴포넌트 컴파일을 위해 필요한 Babel 플러그인들을 자동으로 설치해줍니다. 별다른 추가 설정은 필요하지 않습니다:

```
mix.js('resources/js/app.js', 'public/js')
   .vue();
```

<!-- Once your JavaScript has been compiled, you can reference it in your application: -->
JavaScript가 컴파일된 후에는 다음과 같이 애플리케이션에서 해당 파일을 참조할 수 있습니다:

```html
<head>
    <!-- ... -->

    <script src="/js/app.js"></script>
</head>
```

<a name="react"></a>
<!-- ### React -->
### React

<!-- Mix can automatically install the Babel plugins necessary for React support. To get started, add a call to the `react` method: -->
Mix는 React 지원을 위한 Babel 플러그인도 자동으로 설치해줍니다. 시작하려면 `react` 메서드를 추가로 호출해 주세요:

```
mix.js('resources/js/app.jsx', 'public/js')
   .react();
```

<!-- Behind the scenes, Mix will download and include the appropriate `babel-preset-react` Babel plugin. Once your JavaScript has been compiled, you can reference it in your application: -->
이렇게 하면 내부적으로 Mix가 필요한 `babel-preset-react` Babel 플러그인을 다운로드하여 포함합니다. 컴파일이 끝난 뒤에는 다음과 같이 애플리케이션에서 해당 스크립트를 참조할 수 있습니다:

```html
<head>
    <!-- ... -->

    <script src="/js/app.js"></script>
</head>
```

<a name="vendor-extraction"></a>
<!-- ### Vendor Extraction -->
### Vendor Extraction

<!-- One potential downside to bundling all of your application-specific JavaScript with your vendor libraries such as React and Vue is that it makes long-term caching more difficult. For example, a single update to your application code will force the browser to re-download all of your vendor libraries even if they haven't changed. -->
React, Vue와 같은 벤더 라이브러리를 애플리케이션의 모든 JavaScript와 함께 하나의 파일로 번들링할 경우, 장기 캐싱이 어렵다는 단점이 있습니다. 예를 들어, 애플리케이션 코드가 약간만 변경되어도 브라우저는 벤더 라이브러리 전체를 다시 다운로드해야 할 수 있습니다.

<!-- If you intend to make frequent updates to your application's JavaScript, you should consider extracting all of your vendor libraries into their own file. This way, a change to your application code will not affect the caching of your large `vendor.js` file. Mix's `extract` method makes this a breeze: -->
자주 JavaScript 코드를 업데이트할 예정이라면, 벤더 라이브러리를 별도의 파일로 분리하는 것이 좋습니다. 이렇게 하면 애플리케이션 코드가 바뀌더라도 용량이 큰 `vendor.js`는 캐시로 남게 됩니다. Mix의 `extract` 메서드를 사용하면 이 작업을 쉽게 할 수 있습니다:

```
mix.js('resources/js/app.js', 'public/js')
    .extract(['vue'])
```

<!-- The `extract` method accepts an array of all libraries or modules that you wish to extract into a `vendor.js` file. Using the snippet above as an example, Mix will generate the following files: -->
`extract` 메서드는 `vendor.js` 파일로 분리하고 싶은 모든 라이브러리 또는 모듈의 배열을 인수로 받습니다. 위 예시 코드를 기준으로 Mix는 다음과 같은 파일들을 생성합니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `public/js/manifest.js`: *The Webpack manifest runtime*
- `public/js/vendor.js`: *Your vendor libraries*
- `public/js/app.js`: *Your application code*
-->
- `public/js/manifest.js`: *Webpack 매니페스트 런타임*
- `public/js/vendor.js`: *벤더 라이브러리*
- `public/js/app.js`: *애플리케이션 코드*

<!-- </div> -->
</div>

<!-- To avoid JavaScript errors, be sure to load these files in the proper order: -->
JavaScript 오류를 방지하려면 반드시 아래와 같이 파일들을 올바른 순서로 불러와야 합니다:

```
<script src="/js/manifest.js"></script>
<script src="/js/vendor.js"></script>
<script src="/js/app.js"></script>
```

<a name="custom-webpack-configuration"></a>
<!-- ### Custom Webpack Configuration -->
### Custom Webpack Configuration

<!-- Occasionally, you may need to manually modify the underlying Webpack configuration. For example, you might have a special loader or plugin that needs to be referenced. -->
때로는 직접 Webpack의 하위 설정을 수정해야 할 수도 있습니다. 예를 들어, 커스텀 로더나 플러그인을 추가해야 할 때가 있습니다.

<!-- Mix provides a useful `webpackConfig` method that allows you to merge any short Webpack configuration overrides. This is particularly appealing, as it doesn't require you to copy and maintain your own copy of the `webpack.config.js` file. The `webpackConfig` method accepts an object, which should contain any [Webpack-specific configuration](https://webpack.js.org/configuration/) that you wish to apply. -->
Mix는 `webpackConfig` 메서드를 제공해, 간단한 Webpack 설정을 덮어쓸 수 있게 해줍니다. 이 방식은 별도의 `webpack.config.js` 파일을 복사·유지할 필요 없이 추가적인 설정만 병합할 수 있어서 매우 편리합니다. `webpackConfig`는 객체를 인수로 받아 [Webpack-specific configuration](https://webpack.js.org/configuration/)을 직접 지정할 수 있습니다.

```
mix.webpackConfig({
    resolve: {
        modules: [
            path.resolve(__dirname, 'vendor/laravel/spark/resources/assets/js')
        ]
    }
});
```

<a name="versioning-and-cache-busting"></a>
<!-- ## Versioning / Cache Busting -->
## Versioning / Cache Busting

<!-- Many developers suffix their compiled assets with a timestamp or unique token to force browsers to load the fresh assets instead of serving stale copies of the code. Mix can automatically handle this for you using the `version` method. -->
많은 개발자들은 브라우저가 이전 상태의 에셋을 캐시에 저장하지 않고 항상 최신 에셋을 불러오도록, 컴파일된 파일 이름에 타임스탬프나 고유 토큰을 추가하는 방식을 사용합니다. Mix의 `version` 메서드를 사용하면 이를 자동으로 처리해줍니다.

<!-- The `version` method will append a unique hash to the filenames of all compiled files, allowing for more convenient cache busting: -->
`version` 메서드는 컴파일된 모든 파일 이름 끝에 고유 해시를 추가하여, 캐시 무효화가 훨씬 쉬워집니다:

```
mix.js('resources/js/app.js', 'public/js')
    .version();
```

<!-- After generating the versioned file, you won't know the exact filename. So, you should use Laravel's global `mix` function within your [views](/docs/8.x/views) to load the appropriately hashed asset. The `mix` function will automatically determine the current name of the hashed file: -->
이 과정에서 해시가 포함된 실제 파일 이름을 알기 어렵기 때문에, [views](/docs/8.x/views) 내에서 글로벌 `mix` 함수를 사용해 적절한 파일명을 동적으로 로드해야 합니다. `mix` 함수는 해시가 적용된 현재 파일명을 자동으로 찾아줍니다:

```
<script src="{{ mix('/js/app.js') }}"></script>
```

<!-- Because versioned files are usually unnecessary in development, you may instruct the versioning process to only run during `npm run prod`: -->
대부분 개발 환경에서는 버전 관리가 필요 없으므로, 버전 관리를 `npm run prod` 시에만 실행하도록 설정할 수 있습니다:

```
mix.js('resources/js/app.js', 'public/js');

if (mix.inProduction()) {
    mix.version();
}
```

<a name="custom-mix-base-urls"></a>
<!-- #### Custom Mix Base URLs -->
#### Custom Mix Base URLs

<!-- If your Mix compiled assets are deployed to a CDN separate from your application, you will need to change the base URL generated by the `mix` function. You may do so by adding a `mix_url` configuration option to your application's `config/app.php` configuration file: -->
Mix에서 컴파일된 에셋을 애플리케이션과 별도의 CDN에 배포하는 경우, `mix` 함수가 생성하는 URL의 기본 경로를 변경해야 할 수도 있습니다. 이럴 때는 애플리케이션의 `config/app.php` 설정 파일에 `mix_url` 옵션을 추가하면 됩니다:

```
'mix_url' => env('MIX_ASSET_URL', null)
```

<!-- After configuring the Mix URL, The `mix` function will prefix the configured URL when generating URLs to assets: -->
Mix URL 설정이 완료되면, `mix` 함수가 에셋 링크를 생성할 때 해당 URL을 프리픽스로 붙입니다:

```bash
https://cdn.example.com/js/app.js?id=1964becbdd96414518cd
```

<a name="browsersync-reloading"></a>
<!-- ## Browsersync Reloading -->
## Browsersync Reloading

<!-- [BrowserSync](https://browsersync.io/) can automatically monitor your files for changes, and inject your changes into the browser without requiring a manual refresh. You may enable support for this by calling the `mix.browserSync()` method: -->
[BrowserSync](https://browsersync.io/)를 활용하면 파일 변경 시 브라우저를 수동으로 새로고침하지 않아도, 변경사항을 자동으로 감지해 브라우저에 반영할 수 있습니다. 이 기능은 `mix.browserSync()` 메서드로 쉽게 활성화할 수 있습니다.

```js
mix.browserSync('laravel.test');
```

<!-- [BrowserSync options](https://browsersync.io/docs/options) may be specified by passing a JavaScript object to the `browserSync` method: -->
[BrowserSync options](https://browsersync.io/docs/options)은 `browserSync` 메서드에 JavaScript 객체를 전달하여 지정할 수 있습니다:

```js
mix.browserSync({
    proxy: 'laravel.test'
});
```

<!-- Next, start webpack's development server using the `npm run watch` command. Now, when you modify a script or PHP file you can watch as the browser instantly refreshes the page to reflect your changes. -->
이후, `npm run watch` 명령어로 webpack의 개발 서버를 시작하세요. 이제 스크립트나 PHP 파일을 수정할 때마다 브라우저가 즉시 새로고침되어 변경된 내용을 바로 확인할 수 있습니다.

<a name="environment-variables"></a>
<!-- ## Environment Variables -->
## Environment Variables

<!-- You may inject environment variables into your `webpack.mix.js` script by prefixing one of the environment variables in your `.env` file with `MIX_`: -->
`.env` 파일에서 환경 변수명 앞에 반드시 `MIX_`를 붙이면, 해당 변수를 `webpack.mix.js` 스크립트로 주입할 수 있습니다:

```
MIX_SENTRY_DSN_PUBLIC=http://example.com
```

<!-- After the variable has been defined in your `.env` file, you may access it via the `process.env` object. However, you will need to restart the task if the environment variable's value changes while the task is running: -->
`.env` 파일에 변수를 정의한 후에는, `process.env` 객체를 통해 접근할 수 있습니다. 단, 태스크 실행 중에 환경 변수 값이 바뀌면 태스크를 재시작해야 변경 사항이 적용됩니다:

<!--     process.env.MIX_SENTRY_DSN_PUBLIC -->
    process.env.MIX_SENTRY_DSN_PUBLIC

<a name="notifications"></a>
<!-- ## Notifications -->
## Notifications

<!-- When available, Mix will automatically display OS notifications when compiling, giving you instant feedback as to whether the compilation was successful or not. However, there may be instances when you would prefer to disable these notifications. One such example might be triggering Mix on your production server. Notifications may be deactivated using the `disableNotifications` method: -->
지원되는 환경이라면, Mix는 컴파일 시 자동으로 운영 체제 알림을 표시해 성공 여부를 빠르게 확인할 수 있도록 도와줍니다. 단, 예를 들어 프로덕션 서버에서 Mix를 실행한다면 이런 알림이 불필요할 수 있습니다. 알림을 비활성화하려면 `disableNotifications` 메서드를 사용하면 됩니다:

```
mix.disableNotifications();
```

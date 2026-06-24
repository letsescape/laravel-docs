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
[Laravel Mix](https://github.com/JeffreyWay/laravel-mix) は、[Laracasts](https://laracasts.com) の作成者である Jeffrey Way によって開発されたパッケージで、いくつかの一般的な CSS および JavaScript プリプロセッサを使用して、Laravel アプリケーションの [webpack](https://webpack.js.org) ビルドステップを定義するための流暢な API を提供します。

<!-- In other words, Mix makes it a cinch to compile and minify your application's CSS and JavaScript files. Through simple method chaining, you can fluently define your asset pipeline. For example: -->
言い換えれば、Mix を使用すると、アプリケーションの CSS ファイルと JavaScript ファイルのコンパイルと縮小が簡単になります。シンプルなメソッドチェーンを通じて、アセットパイプラインをスムーズに定義できます。例えば：

```
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

<!-- If you've ever been confused and overwhelmed about getting started with webpack and asset compilation, you will love Laravel Mix. However, you are not required to use it while developing your application; you are free to use any asset pipeline tool you wish, or even none at all. -->
Webpack とアセットのコンパイルを開始する際に混乱したり圧倒されたりしたことがあれば、Laravel Mix を気に入るはずです。ただし、アプリケーションの開発中にこれを使用する必要はありません。希望するアセット パイプライン ツールを自由に使用することも、まったく使用しないこともできます。

> [!TIP]
> Laravel と [Tailwind CSS](https://tailwindcss.com) を使用してアプリケーションの構築をすぐに始める必要がある場合は、[application starter kits](/docs/8.x/starter-kits) のいずれかをチェックしてください。

<a name="installation"></a>
<!-- ## Installation & Setup -->
## Installation & Setup

<a name="installing-node"></a>
<!-- #### Installing Node -->
#### Installing Node

<!-- Before running Mix, you must first ensure that Node.js and NPM are installed on your machine: -->
Mix を実行する前に、まず Node.js と NPM がマシンにインストールされていることを確認する必要があります。

```
node -v
npm -v
```

<!-- You can easily install the latest version of Node and NPM using simple graphical installers from [the official Node website](https://nodejs.org/en/download/). Or, if you are using [Laravel Sail](/docs/8.x/sail), you may invoke Node and NPM through Sail: -->
[the official Node website](https://nodejs.org/en/download/) のシンプルなグラフィカル インストーラーを使用して、Node と NPM の最新バージョンを簡単にインストールできます。または、[Laravel Sail](/docs/8.x/sail) を使用している場合は、Sail を通じて Node と NPM を呼び出すことができます。

```
./sail node -v
./sail npm -v
```

<a name="installing-laravel-mix"></a>
<!-- #### Installing Laravel Mix -->
#### Installing Laravel Mix

<!-- The only remaining step is to install Laravel Mix. Within a fresh installation of Laravel, you'll find a `package.json` file in the root of your directory structure. The default `package.json` file already includes everything you need to get started using Laravel Mix. Think of this file like your `composer.json` file, except it defines Node dependencies instead of PHP dependencies. You may install the dependencies it references by running: -->
残っている唯一の手順は、Laravel Mix をインストールすることです。 Laravel を新規インストールすると、ディレクトリ構造のルートに `package.json` ファイルが見つかります。デフォルトの `package.json` ファイルには、Laravel Mix の使用を開始するために必要なものがすべて含まれています。このファイルは、PHP 依存関係ではなくノード依存関係を定義する点を除いて、`composer.json` ファイルと同じように考えてください。以下を実行して、参照する依存関係をインストールできます。

```
npm install
```

<a name="running-mix"></a>
<!-- ## Running Mix -->
## Running Mix

<!-- Mix is a configuration layer on top of [webpack](https://webpack.js.org), so to run your Mix tasks you only need to execute one of the NPM scripts that are included in the default Laravel `package.json` file. When you run the `dev` or `production` scripts, all of your application's CSS and JavaScript assets will be compiled and placed in your application's `public` directory: -->
Mix は [webpack](https://webpack.js.org) の上にある構成レイヤーであるため、Mix タスクを実行するには、デフォルトの Laravel `package.json` ファイルに含まれている NPM スクリプトの 1 つを実行するだけで済みます。 `dev` または `production` スクリプトを実行すると、アプリケーションのすべての CSS および JavaScript アセットがコンパイルされ、アプリケーションの `public` ディレクトリに配置されます。

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
`npm run watch` コマンドはターミナルで実行を継続し、関連するすべての CSS および JavaScript ファイルの変更を監視します。 Webpack は、次のファイルのいずれかに対する変更を検出すると、アセットを自動的に再コンパイルします。

```
npm run watch
```

<!-- Webpack may not be able to detect your file changes in certain local development environments. If this is the case on your system, consider using the `watch-poll` command: -->
Webpack は、特定のローカル開発環境ではファイルの変更を検出できない場合があります。これがシステムに当てはまる場合は、`watch-poll` コマンドの使用を検討してください。

```
npm run watch-poll
```

<a name="working-with-stylesheets"></a>
<!-- ## Working With Stylesheets -->
## Working With Stylesheets

<!-- Your application's `webpack.mix.js` file is your entry point for all asset compilation. Think of it as a light configuration wrapper around [webpack](https://webpack.js.org). Mix tasks can be chained together to define exactly how your assets should be compiled. -->
アプリケーションの `webpack.mix.js` ファイルは、すべてのアセット コンパイルのエントリ ポイントです。これは、[webpack](https://webpack.js.org) の軽量構成ラッパーと考えてください。Mix タスクを連鎖させて、アセットのコンパイル方法を正確に定義できます。

<a name="tailwindcss"></a>
<!-- ### Tailwind CSS -->
### Tailwind CSS

<!-- [Tailwind CSS](https://tailwindcss.com) is a modern, utility-first framework for building amazing sites without ever leaving your HTML. Let's dig into how to start using it in a Laravel project with Laravel Mix. First, we should install Tailwind using NPM and generate our Tailwind configuration file: -->
[Tailwind CSS](https://tailwindcss.com) は、HTML を離れることなく素晴らしいサイトを構築できる、実用性を第一に考えた最新のフレームワークです。 Laravel Mix を使用して Laravel プロジェクトでそれを使い始める方法を詳しく見てみましょう。まず、NPM を使用して Tailwind をインストールし、Tailwind 構成ファイルを生成する必要があります。

```
npm install

npm install -D tailwindcss

npx tailwindcss init
```

<!-- The `init` command will generate a `tailwind.config.js` file. The `content` section of this file allows you to configure the paths to all of your HTML templates, JavaScript components, and any other source files that contain Tailwind class names so that any CSS classes that are not used within these files will be purged from your production CSS build: -->
`init` コマンドは、`tailwind.config.js` ファイルを生成します。このファイルの `content` セクションでは、すべての HTML テンプレート、JavaScript コンポーネント、および Tailwind クラス名を含むその他のソース ファイルへのパスを構成して、これらのファイル内で使用されていない CSS クラスが運用環境の CSS ビルドから削除されるようにすることができます。

```js
content: [
    './storage/framework/views/*.php',
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './resources/**/*.vue',
],
```

<!-- Next, you should add each of Tailwind's "layers" to your application's `resources/css/app.css` file: -->
次に、Tailwind の各「レイヤー」をアプリケーションの `resources/css/app.css` ファイルに追加する必要があります。

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

<!-- Once you have configured Tailwind's layers, you are ready to update your application's `webpack.mix.js` file to compile your Tailwind powered CSS: -->
Tailwind のレイヤーを構成したら、アプリケーションの `webpack.mix.js` ファイルを更新して、Tailwind を利用した CSS をコンパイルする準備が整います。

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css', [
        require('tailwindcss'),
    ]);
```

<!-- Finally, you should reference your stylesheet in your application's primary layout template. Many applications choose to store this template at `resources/views/layouts/app.blade.php`. In addition, ensure you add the responsive viewport `meta` tag if it's not already present: -->
最後に、アプリケーションのプライマリ レイアウト テンプレートでスタイルシートを参照する必要があります。多くのアプリケーションは、このテンプレートを `resources/views/layouts/app.blade.php` に保存することを選択します。さらに、レスポンシブ ビューポート `meta` タグがまだ存在しない場合は、必ず追加してください。

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
CSS を変換するための強力なツールである [PostCSS](https://postcss.org/) は、すぐに使える Laravel Mix に含まれています。デフォルトでは、Mix は人気のある [Autoprefixer](https://github.com/postcss/autoprefixer) プラグインを利用して、必要な CSS3 ベンダー プレフィックスをすべて自動的に適用します。ただし、アプリケーションに適したプラグインを自由に追加できます。

<!-- First, install the desired plugin through NPM and include it in your array of plugins when calling Mix's `postCss` method. The `postCss` method accepts the path to your CSS file as its first argument and the directory where the compiled file should be placed as its second argument: -->
まず、NPM を通じて目的のプラグインをインストールし、Mix の `postCss` メソッドを呼び出すときにそれをプラグインの配列に含めます。 `postCss` メソッドは、CSS ファイルへのパスを最初の引数として受け入れ、コンパイルされたファイルを配置するディレクトリを 2 番目の引数として受け入れます。

```
mix.postCss('resources/css/app.css', 'public/css', [
    require('postcss-custom-properties')
]);
```

<!-- Or, you may execute `postCss` with no additional plugins in order to achieve simple CSS compilation and minification: -->
または、単純な CSS コンパイルと縮小を実現するために、追加のプラグインを使用せずに `postCss` を実行することもできます。

```
mix.postCss('resources/css/app.css', 'public/css');
```

<a name="sass"></a>
<!-- ### Sass -->
### Sass

<!-- The `sass` method allows you to compile [Sass](https://sass-lang.com/) into CSS that can be understood by web browsers. The `sass` method accepts the path to your Sass file as its first argument and the directory where the compiled file should be placed as its second argument: -->
`sass` メソッドを使用すると、[Sass](https://sass-lang.com/) を Web ブラウザーが理解できる CSS にコンパイルできます。 `sass` メソッドは、Sass ファイルへのパスを最初の引数として受け入れ、コンパイルされたファイルを配置するディレクトリを 2 番目の引数として受け入れます。

```
mix.sass('resources/sass/app.scss', 'public/css');
```

<!-- You may compile multiple Sass files into their own respective CSS files and even customize the output directory of the resulting CSS by calling the `sass` method multiple times: -->
複数の Sass ファイルをそれぞれ独自の CSS ファイルにコンパイルしたり、`sass` メソッドを複数回呼び出して、結果の CSS の出力ディレクトリをカスタマイズしたりすることもできます。

```
mix.sass('resources/sass/app.sass', 'public/css')
    .sass('resources/sass/admin.sass', 'public/css/admin');
```

<a name="url-processing"></a>
<!-- ### URL Processing -->
### URL Processing

<!-- Because Laravel Mix is built on top of webpack, it's important to understand a few webpack concepts. For CSS compilation, webpack will rewrite and optimize any `url()` calls within your stylesheets. While this might initially sound strange, it's an incredibly powerful piece of functionality. Imagine that we want to compile Sass that includes a relative URL to an image: -->
Laravel Mix は webpack 上に構築されているため、webpack の概念をいくつか理解することが重要です。 CSS コンパイルの場合、webpack はスタイルシート内の `url()` 呼び出しを書き換えて最適化します。最初は奇妙に聞こえるかもしれませんが、これは非常に強力な機能です。画像への相対 URL を含む Sass をコンパイルするとします。

```
.example {
    background: url('../images/example.png');
}
```

> [!NOTE]
> 特定の `url()` の絶対パスは URL 書き換えから除外されます。たとえば、`url('/images/thing.png')` または `url('http://example.com/images/thing.png')` は変更されません。

<!-- By default, Laravel Mix and webpack will find `example.png`, copy it to your `public/images` folder, and then rewrite the `url()` within your generated stylesheet. As such, your compiled CSS will be: -->
デフォルトでは、Laravel Mix と webpack は `example.png` を見つけて `public/images` フォルダーにコピーし、生成されたスタイルシート内の `url()` を書き換えます。そのため、コンパイルされた CSS は次のようになります。

```
.example {
    background: url(/images/example.png?d41d8cd98f00b204e9800998ecf8427e);
}
```

<!-- As useful as this feature may be, your existing folder structure may already be configured in a way you like. If this is the case, you may disable `url()` rewriting like so: -->
この機能は便利ですが、既存のフォルダー構造がすでに好みの方法で構成されている可能性があります。この場合は、次のように `url()` の書き換えを無効にすることができます。

```
mix.sass('resources/sass/app.scss', 'public/css').options({
    processCssUrls: false
});
```

<!-- With this addition to your `webpack.mix.js` file, Mix will no longer match any `url()` or copy assets to your public directory. In other words, the compiled CSS will look just like how you originally typed it: -->
これを `webpack.mix.js` ファイルに追加すると、Mix は `url()` と一致しなくなり、アセットをパブリック ディレクトリにコピーしなくなります。つまり、コンパイルされた CSS は、最初に入力したものとまったく同じようになります。

```
.example {
    background: url("../images/thing.png");
}
```

<a name="css-source-maps"></a>
<!-- ### Source Maps -->
### Source Maps

<!-- Though disabled by default, source maps may be activated by calling the `mix.sourceMaps()` method in your `webpack.mix.js` file. Though it comes with a compile/performance cost, this will provide extra debugging information to your browser's developer tools when using compiled assets: -->
デフォルトでは無効になっていますが、ソース マップは、`webpack.mix.js` ファイル内の `mix.sourceMaps()` メソッドを呼び出すことでアクティブ化できます。コンパイル/パフォーマンスのコストがかかりますが、コンパイルされたアセットを使用するときにブラウザの開発者ツールに追加のデバッグ情報が提供されます。

```
mix.js('resources/js/app.js', 'public/js')
    .sourceMaps();
```

<a name="style-of-source-mapping"></a>
<!-- #### Style Of Source Mapping -->
#### Style Of Source Mapping

<!-- Webpack offers a variety of [source mapping styles](https://webpack.js.org/configuration/devtool/#devtool). By default, Mix's source mapping style is set to `eval-source-map`, which provides a fast rebuild time. If you want to change the mapping style, you may do so using the `sourceMaps` method: -->
Webpack はさまざまな [source mapping styles](https://webpack.js.org/configuration/devtool/#devtool) を提供しています。デフォルトでは、Mix のソース マッピング スタイルは `eval-source-map` に設定されており、リビルド時間が短縮されます。マッピング スタイルを変更したい場合は、`sourceMaps` メソッドを使用して変更できます。

```
let productionSourceMaps = false;

mix.js('resources/js/app.js', 'public/js')
    .sourceMaps(productionSourceMaps, 'source-map');
```

<a name="working-with-scripts"></a>
<!-- ## Working With JavaScript -->
## Working With JavaScript

<!-- Mix provides several features to help you work with your JavaScript files, such as compiling modern ECMAScript, module bundling, minification, and concatenating plain JavaScript files. Even better, this all works seamlessly, without requiring an ounce of custom configuration: -->
Mix は、最新の ECMAScript のコンパイル、モジュールのバンドル、縮小化、プレーン JavaScript ファイルの連結など、JavaScript ファイルの操作に役立つ機能をいくつか提供します。さらに良いのは、カスタム構成をまったく必要とせずに、これがすべてシームレスに機能することです。

```
mix.js('resources/js/app.js', 'public/js');
```

<!-- With this single line of code, you may now take advantage of: -->
この 1 行のコードで、次の機能を利用できるようになります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The latest EcmaScript syntax.
- Modules
- Minification for production environments.
-->
- 最新の EcmaScript 構文。
- モジュール
- 本番環境向けの縮小化。

<!-- </div> -->
</div>

<a name="vue"></a>
<!-- ### Vue -->
### Vue

<!-- Mix will automatically install the Babel plugins necessary for Vue single-file component compilation support when using the `vue` method. No further configuration is required: -->
Mix は、`vue` メソッドを使用する場合、Vue の単一ファイル コンポーネントのコンパイル サポートに必要な Babel プラグインを自動的にインストールします。これ以上の構成は必要ありません。

```
mix.js('resources/js/app.js', 'public/js')
   .vue();
```

<!-- Once your JavaScript has been compiled, you can reference it in your application: -->
JavaScript がコンパイルされたら、アプリケーション内でそれを参照できます。

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
Mix は、React サポートに必要な Babel プラグインを自動的にインストールできます。まず、`react` メソッドへの呼び出しを追加します。

```
mix.js('resources/js/app.jsx', 'public/js')
   .react();
```

<!-- Behind the scenes, Mix will download and include the appropriate `babel-preset-react` Babel plugin. Once your JavaScript has been compiled, you can reference it in your application: -->
Mix は舞台裏で、適切な `babel-preset-react` Babel プラグインをダウンロードしてインクルードします。 JavaScript がコンパイルされたら、アプリケーション内でそれを参照できます。

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
アプリケーション固有の JavaScript をすべて React や Vue などのベンダー ライブラリにバンドルすることの潜在的な欠点の 1 つは、長期的なキャッシュがより困難になることです。たとえば、アプリケーション コードを 1 回更新すると、ベンダー ライブラリが変更されていない場合でも、ブラウザはすべてのベンダー ライブラリを強制的に再ダウンロードします。

<!-- If you intend to make frequent updates to your application's JavaScript, you should consider extracting all of your vendor libraries into their own file. This way, a change to your application code will not affect the caching of your large `vendor.js` file. Mix's `extract` method makes this a breeze: -->
アプリケーションの JavaScript を頻繁に更新する場合は、すべてのベンダー ライブラリを独自のファイルに抽出することを検討する必要があります。こうすることで、アプリケーション コードを変更しても、大きな `vendor.js` ファイルのキャッシュに影響を与えることはありません。 Mix の `extract` メソッドを使用すると、これが簡単になります。

```
mix.js('resources/js/app.js', 'public/js')
    .extract(['vue'])
```

<!-- The `extract` method accepts an array of all libraries or modules that you wish to extract into a `vendor.js` file. Using the snippet above as an example, Mix will generate the following files: -->
`extract` メソッドは、`vendor.js` ファイルに抽出するすべてのライブラリまたはモジュールの配列を受け入れます。上記のスニペットを例として使用すると、Mix は次のファイルを生成します。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `public/js/manifest.js`: *The Webpack manifest runtime*
- `public/js/vendor.js`: *Your vendor libraries*
- `public/js/app.js`: *Your application code*
-->
- `public/js/manifest.js`: *Webpack マニフェスト ランタイム*
- `public/js/vendor.js`: *ベンダー ライブラリ*
- `public/js/app.js`: *アプリケーション コード*

<!-- </div> -->
</div>

<!-- To avoid JavaScript errors, be sure to load these files in the proper order: -->
JavaScript エラーを回避するには、次のファイルを正しい順序でロードしてください。

```
<script src="/js/manifest.js"></script>
<script src="/js/vendor.js"></script>
<script src="/js/app.js"></script>
```

<a name="custom-webpack-configuration"></a>
<!-- ### Custom Webpack Configuration -->
### Custom Webpack Configuration

<!-- Occasionally, you may need to manually modify the underlying Webpack configuration. For example, you might have a special loader or plugin that needs to be referenced. -->
場合によっては、基礎となる Webpack 構成を手動で変更する必要がある場合があります。たとえば、参照する必要がある特別なローダーまたはプラグインがある場合があります。

<!-- Mix provides a useful `webpackConfig` method that allows you to merge any short Webpack configuration overrides. This is particularly appealing, as it doesn't require you to copy and maintain your own copy of the `webpack.config.js` file. The `webpackConfig` method accepts an object, which should contain any [Webpack-specific configuration](https://webpack.js.org/configuration/) that you wish to apply. -->
Mix は、短い Webpack 構成オーバーライドをマージできる便利な `webpackConfig` メソッドを提供します。これは、`webpack.config.js` ファイルの独自のコピーをコピーして管理する必要がないため、特に魅力的です。 `webpackConfig` メソッドはオブジェクトを受け入れます。このオブジェクトには、適用する [Webpack-specific configuration](https://webpack.js.org/configuration/) が含まれている必要があります。

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
多くの開発者は、コンパイルされたアセットの末尾にタイムスタンプまたは一意のトークンを付けて、コードの古いコピーを提供するのではなく、ブラウザーに新しいアセットを強制的にロードさせます。 Mix は、`version` メソッドを使用してこれを自動的に処理できます。

<!-- The `version` method will append a unique hash to the filenames of all compiled files, allowing for more convenient cache busting: -->
`version` メソッドは、コンパイルされたすべてのファイルのファイル名に一意のハッシュを追加し、より便利なキャッシュ無効化を可能にします。

```
mix.js('resources/js/app.js', 'public/js')
    .version();
```

<!-- After generating the versioned file, you won't know the exact filename. So, you should use Laravel's global `mix` function within your [views](/docs/8.x/views) to load the appropriately hashed asset. The `mix` function will automatically determine the current name of the hashed file: -->
バージョン管理されたファイルを生成した後は、正確なファイル名はわかりません。したがって、適切にハッシュされたアセットをロードするには、[views](/docs/8.x/views) 内で Laravel のグローバル `mix` 関数を使用する必要があります。 `mix` 関数は、ハッシュされたファイルの現在の名前を自動的に決定します。

```
<script src="{{ mix('/js/app.js') }}"></script>
```

<!-- Because versioned files are usually unnecessary in development, you may instruct the versioning process to only run during `npm run prod`: -->
バージョン管理されたファイルは通常、開発では不要であるため、`npm run prod` 中にのみ実行するようにバージョン管理プロセスを指示できます。

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
Mix でコンパイルされたアセットがアプリケーションとは別の CDN にデプロイされている場合は、`mix` 関数によって生成されたベース URL を変更する必要があります。これを行うには、アプリケーションの `config/app.php` 構成ファイルに `mix_url` 構成オプションを追加します。

```
'mix_url' => env('MIX_ASSET_URL', null)
```

<!-- After configuring the Mix URL, The `mix` function will prefix the configured URL when generating URLs to assets: -->
Mix URL を構成した後、`mix` 関数は、アセットへの URL を生成するときに、構成された URL にプレフィックスを付けます。

```bash
https://cdn.example.com/js/app.js?id=1964becbdd96414518cd
```

<a name="browsersync-reloading"></a>
<!-- ## Browsersync Reloading -->
## Browsersync Reloading

<!-- [BrowserSync](https://browsersync.io/) can automatically monitor your files for changes, and inject your changes into the browser without requiring a manual refresh. You may enable support for this by calling the `mix.browserSync()` method: -->
[BrowserSync](https://browsersync.io/) は、ファイルの変更を自動的に監視し、手動で更新することなく変更をブラウザに挿入できます。 `mix.browserSync()` メソッドを呼び出すことで、これのサポートを有効にすることができます。

```js
mix.browserSync('laravel.test');
```

<!-- [BrowserSync options](https://browsersync.io/docs/options) may be specified by passing a JavaScript object to the `browserSync` method: -->
[BrowserSync options](https://browsersync.io/docs/options) は、JavaScript オブジェクトを `browserSync` メソッドに渡すことで指定できます。

```js
mix.browserSync({
    proxy: 'laravel.test'
});
```

<!-- Next, start webpack's development server using the `npm run watch` command. Now, when you modify a script or PHP file you can watch as the browser instantly refreshes the page to reflect your changes. -->
次に、`npm run watch` コマンドを使用して webpack の開発サーバーを起動します。スクリプトまたは PHP ファイルを変更すると、ブラウザが即座にページを更新して変更を反映するのを確認できるようになりました。

<a name="environment-variables"></a>
<!-- ## Environment Variables -->
## Environment Variables

<!-- You may inject environment variables into your `webpack.mix.js` script by prefixing one of the environment variables in your `.env` file with `MIX_`: -->
`.env` ファイル内の環境変数の 1 つに `MIX_` というプレフィックスを付けることで、環境変数を `webpack.mix.js` スクリプトに挿入できます。

```
MIX_SENTRY_DSN_PUBLIC=http://example.com
```

<!-- After the variable has been defined in your `.env` file, you may access it via the `process.env` object. However, you will need to restart the task if the environment variable's value changes while the task is running: -->
変数が `.env` ファイルで定義されたら、`process.env` オブジェクトを介して変数にアクセスできます。ただし、タスクの実行中に環境変数の値が変更された場合は、タスクを再起動する必要があります。

<!--     process.env.MIX_SENTRY_DSN_PUBLIC -->
    process.env.MIX_SENTRY_DSN_PUBLIC

<a name="notifications"></a>
<!-- ## Notifications -->
## Notifications

<!-- When available, Mix will automatically display OS notifications when compiling, giving you instant feedback as to whether the compilation was successful or not. However, there may be instances when you would prefer to disable these notifications. One such example might be triggering Mix on your production server. Notifications may be deactivated using the `disableNotifications` method: -->
利用可能な場合、Mix はコンパイル時に OS 通知を自動的に表示し、コンパイルが成功したかどうかについて即座にフィードバックを提供します。ただし、これらの通知を無効にした方がよい場合もあります。そのような例の 1 つは、運用サーバー上で Mix をトリガーすることです。通知は、`disableNotifications` メソッドを使用して非アクティブ化できます。

```
mix.disableNotifications();
```


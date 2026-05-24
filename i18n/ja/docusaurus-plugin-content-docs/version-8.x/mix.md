# アセットのコンパイル (Mix) (Compiling Assets (Mix))

- [Introduction](#introduction)
- [インストールとセットアップ](#installation)
- [Mix の実行](#running-mix)
- [スタイルシートの操作](#working-with-stylesheets)
    - [Tailwind CSS](#tailwindcss)
    - [PostCSS](#postcss)
    - [Sass](#sass)
    - [URL処理](#url-processing)
    - [ソースマップ](#css-source-maps)
- [JavaScript の操作](#working-with-scripts)
    - [Vue](#vue)
    - [React](#react)
    - [ベンダーの抽出](#vendor-extraction)
    - [カスタム Webpack 構成](#custom-webpack-configuration)
- [バージョニング/キャッシュバスティング](#versioning-and-cache-busting)
- [ブラウザ同期のリロード](#browsersync-reloading)
- [環境変数](#environment-variables)
- [Notifications](#notifications)

<a name="introduction"></a>
## 導入 (Introduction)

[Laracasts](https://github.com/JeffreyWay/laravel-mix) の作成者である Jeffrey Way によって開発されたパッケージである [Laravel Mix](https://laracasts.com) は、いくつかの一般的な CSS および JavaScript プリプロセッサを使用して、Laravel アプリケーションの [webpack](https://webpack.js.org) ビルドステップを定義するための流暢な API を提供します。

言い換えれば、Mix を使用すると、アプリケーションの CSS ファイルと JavaScript ファイルのコンパイルと縮小が簡単になります。シンプルなメソッドチェーンを通じて、アセットパイプラインをスムーズに定義できます。例えば：

    mix.js('resources/js/app.js', 'public/js')
        .postCss('resources/css/app.css', 'public/css');

Webpack とアセットのコンパイルを開始する際に混乱したり圧倒されたりしたことがあれば、Laravel Mix を気に入るはずです。ただし、アプリケーションの開発中にこれを使用する必要はありません。希望するアセット パイプライン ツールを自由に使用することも、まったく使用しないこともできます。

> {tip} Laravel と [Tailwind CSS](https://tailwindcss.com) を使用してアプリケーションの構築をすぐに始める必要がある場合は、[アプリケーションスターターキット](/docs/{{version}}/starter-kits) のいずれかをチェックしてください。

<a name="installation"></a>
## インストールとセットアップ (Installation & Setup)

<a name="installing-node"></a>
#### ノードのインストール

Mix を実行する前に、まず Node.js と NPM がマシンにインストールされていることを確認する必要があります。

    node -v
    npm -v

[ノードの公式ウェブサイト](https://nodejs.org/en/download/) のシンプルなグラフィカル インストーラーを使用して、Node と NPM の最新バージョンを簡単にインストールできます。または、[Laravel Sail](/docs/{{version}}/sail) を使用している場合は、Sail を通じて Node と NPM を呼び出すことができます。

    ./sail node -v
    ./sail npm -v

<a name="installing-laravel-mix"></a>
#### Laravel Mixのインストール

残っている唯一の手順は、Laravel Mix をインストールすることです。 Laravel を新規インストールすると、ディレクトリ構造のルートに `package.json` ファイルが見つかります。デフォルトの `package.json` ファイルには、Laravel Mix の使用を開始するために必要なものがすべて含まれています。このファイルは、PHP 依存関係ではなくノード依存関係を定義する点を除いて、`composer.json` ファイルと同じように考えてください。以下を実行して、参照する依存関係をインストールできます。

    npm install

<a name="running-mix"></a>
## Mix の実行 (Running Mix)

Mix は [webpack](https://webpack.js.org) の上にある構成レイヤーであるため、Mix タスクを実行するには、デフォルトの Laravel `package.json` ファイルに含まれている NPM スクリプトの 1 つを実行するだけで済みます。 `dev` または `production` スクリプトを実行すると、アプリケーションのすべての CSS および JavaScript アセットがコンパイルされ、アプリケーションの `public` ディレクトリに配置されます。

    // Run all Mix tasks...
    npm run dev

    // Run all Mix tasks and minify output...
    npm run prod

<a name="watching-assets-for-changes"></a>
#### アセットの変化を監視する

`npm run watch` コマンドはターミナルで実行を継続し、関連するすべての CSS および JavaScript ファイルの変更を監視します。 Webpack は、次のファイルのいずれかに対する変更を検出すると、アセットを自動的に再コンパイルします。

    npm run watch

Webpack は、特定のローカル開発環境ではファイルの変更を検出できない場合があります。これがシステムに当てはまる場合は、`watch-poll` コマンドの使用を検討してください。

    npm run watch-poll

<a name="working-with-stylesheets"></a>
## スタイルシートの操作 (Working With Stylesheets)

アプリケーションの `webpack.mix.js` ファイルは、すべてのアセット コンパイルのエントリ ポイントです。これは、[webpack](https://webpack.js.org) の軽量構成ラッパーと考えてください。Mix タスクを連鎖させて、アセットのコンパイル方法を正確に定義できます。

<a name="tailwindcss"></a>
### Tailwind CSS

[Tailwind CSS](https://tailwindcss.com) は、HTML を離れることなく素晴らしいサイトを構築できる、実用性を第一に考えた最新のフレームワークです。 Laravel Mix を使用して Laravel プロジェクトでそれを使い始める方法を詳しく見てみましょう。まず、NPM を使用して Tailwind をインストールし、Tailwind 構成ファイルを生成する必要があります。

    npm install

    npm install -D tailwindcss

    npx tailwindcss init

`init` コマンドは、`tailwind.config.js` ファイルを生成します。このファイルの `content` セクションでは、すべての HTML テンプレート、JavaScript コンポーネント、および Tailwind クラス名を含むその他のソース ファイルへのパスを構成して、これらのファイル内で使用されていない CSS クラスが運用環境の CSS ビルドから削除されるようにすることができます。

```js
content: [
    './storage/framework/views/*.php',
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './resources/**/*.vue',
],
```

次に、Tailwind の各「レイヤー」をアプリケーションの `resources/css/app.css` ファイルに追加する必要があります。

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Tailwind のレイヤーを構成したら、アプリケーションの `webpack.mix.js` ファイルを更新して、Tailwind を利用した CSS をコンパイルする準備が整います。

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css', [
        require('tailwindcss'),
    ]);
```

最後に、アプリケーションのプライマリ レイアウト テンプレートでスタイルシートを参照する必要があります。多くのアプリケーションは、このテンプレートを `resources/views/layouts/app.blade.php` に保存することを選択します。さらに、レスポンシブ ビューポート `meta` タグがまだ存在しない場合は、必ず追加してください。

```html
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href="/css/app.css" rel="stylesheet">
</head>
```

<a name="postcss"></a>
### PostCSS

CSS を変換するための強力なツールである [PostCSS](https://postcss.org/) は、すぐに使える Laravel Mix に含まれています。デフォルトでは、Mix は人気のある [Autoprefixer](https://github.com/postcss/autoprefixer) プラグインを利用して、必要な CSS3 ベンダー プレフィックスをすべて自動的に適用します。ただし、アプリケーションに適したプラグインを自由に追加できます。

まず、NPM を通じて目的のプラグインをインストールし、Mix の `postCss` メソッドを呼び出すときにそれをプラグインの配列に含めます。 `postCss` メソッドは、CSS ファイルへのパスを最初の引数として受け入れ、コンパイルされたファイルを配置するディレクトリを 2 番目の引数として受け入れます。

    mix.postCss('resources/css/app.css', 'public/css', [
        require('postcss-custom-properties')
    ]);

または、単純な CSS コンパイルと縮小を実現するために、追加のプラグインを使用せずに `postCss` を実行することもできます。

    mix.postCss('resources/css/app.css', 'public/css');

<a name="sass"></a>
### サス

`sass` メソッドを使用すると、[Sass](https://sass-lang.com/) を Web ブラウザーが理解できる CSS にコンパイルできます。 `sass` メソッドは、Sass ファイルへのパスを最初の引数として受け入れ、コンパイルされたファイルを配置するディレクトリを 2 番目の引数として受け入れます。

    mix.sass('resources/sass/app.scss', 'public/css');

複数の Sass ファイルをそれぞれ独自の CSS ファイルにコンパイルしたり、`sass` メソッドを複数回呼び出して、結果の CSS の出力ディレクトリをカスタマイズしたりすることもできます。

    mix.sass('resources/sass/app.sass', 'public/css')
        .sass('resources/sass/admin.sass', 'public/css/admin');

<a name="url-processing"></a>
### URL処理

Laravel Mix は webpack 上に構築されているため、webpack の概念をいくつか理解することが重要です。 CSS コンパイルの場合、webpack はスタイルシート内の `url()` 呼び出しを書き換えて最適化します。最初は奇妙に聞こえるかもしれませんが、これは非常に強力な機能です。画像への相対 URL を含む Sass をコンパイルするとします。

    .example {
        background: url('../images/example.png');
    }

> {note} 特定の `url()` の絶対パスは URL 書き換えから除外されます。たとえば、`url('/images/thing.png')` または `url('http://example.com/images/thing.png')` は変更されません。

デフォルトでは、Laravel Mix と webpack は `example.png` を見つけて `public/images` フォルダーにコピーし、生成されたスタイルシート内の `url()` を書き換えます。そのため、コンパイルされた CSS は次のようになります。

    .example {
        background: url(/images/example.png?d41d8cd98f00b204e9800998ecf8427e);
    }

この機能は便利ですが、既存のフォルダー構造がすでに好みの方法で構成されている可能性があります。この場合は、次のように `url()` の書き換えを無効にすることができます。

    mix.sass('resources/sass/app.scss', 'public/css').options({
        processCssUrls: false
    });

これを `webpack.mix.js` ファイルに追加すると、Mix は `url()` と一致しなくなり、アセットをパブリック ディレクトリにコピーしなくなります。つまり、コンパイルされた CSS は、最初に入力したものとまったく同じようになります。

    .example {
        background: url("../images/thing.png");
    }

<a name="css-source-maps"></a>
### ソースマップ

デフォルトでは無効になっていますが、ソース マップは、`webpack.mix.js` ファイル内の `mix.sourceMaps()` メソッドを呼び出すことでアクティブ化できます。コンパイル/パフォーマンスのコストがかかりますが、コンパイルされたアセットを使用するときにブラウザの開発者ツールに追加のデバッグ情報が提供されます。

    mix.js('resources/js/app.js', 'public/js')
        .sourceMaps();

<a name="style-of-source-mapping"></a>
#### ソースマッピングのスタイル

Webpack はさまざまな [ソースマッピングスタイル](https://webpack.js.org/configuration/devtool/#devtool) を提供しています。デフォルトでは、Mix のソース マッピング スタイルは `eval-source-map` に設定されており、リビルド時間が短縮されます。マッピング スタイルを変更したい場合は、`sourceMaps` メソッドを使用して変更できます。

    let productionSourceMaps = false;

    mix.js('resources/js/app.js', 'public/js')
        .sourceMaps(productionSourceMaps, 'source-map');

<a name="working-with-scripts"></a>
## JavaScript の操作 (Working With JavaScript)

Mix は、最新の ECMAScript のコンパイル、モジュールのバンドル、縮小化、プレーン JavaScript ファイルの連結など、JavaScript ファイルの操作に役立つ機能をいくつか提供します。さらに良いのは、カスタム構成をまったく必要とせずに、これがすべてシームレスに機能することです。

    mix.js('resources/js/app.js', 'public/js');

この 1 行のコードで、次の機能を利用できるようになります。

<div class="content-list" markdown="1">

- 最新の EcmaScript 構文。
- モジュール
- 本番環境向けの縮小化。

</div>

<a name="vue"></a>
### ヴュー

Mix は、`vue` メソッドを使用する場合、Vue の単一ファイル コンポーネントのコンパイル サポートに必要な Babel プラグインを自動的にインストールします。これ以上の構成は必要ありません。

    mix.js('resources/js/app.js', 'public/js')
       .vue();

JavaScript がコンパイルされたら、アプリケーション内でそれを参照できます。

```html
<head>
    <!-- ... -->

    <script src="/js/app.js"></script>
</head>
```

<a name="react"></a>
### 反応する

Mix は、React サポートに必要な Babel プラグインを自動的にインストールできます。まず、`react` メソッドへの呼び出しを追加します。

    mix.js('resources/js/app.jsx', 'public/js')
       .react();

Mix は舞台裏で、適切な `babel-preset-react` Babel プラグインをダウンロードしてインクルードします。 JavaScript がコンパイルされたら、アプリケーション内でそれを参照できます。

```html
<head>
    <!-- ... -->

    <script src="/js/app.js"></script>
</head>
```

<a name="vendor-extraction"></a>
### ベンダーの抽出

アプリケーション固有の JavaScript をすべて React や Vue などのベンダー ライブラリにバンドルすることの潜在的な欠点の 1 つは、長期的なキャッシュがより困難になることです。たとえば、アプリケーション コードを 1 回更新すると、ベンダー ライブラリが変更されていない場合でも、ブラウザはすべてのベンダー ライブラリを強制的に再ダウンロードします。

アプリケーションの JavaScript を頻繁に更新する場合は、すべてのベンダー ライブラリを独自のファイルに抽出することを検討する必要があります。こうすることで、アプリケーション コードを変更しても、大きな `vendor.js` ファイルのキャッシュに影響を与えることはありません。 Mix の `extract` メソッドを使用すると、これが簡単になります。

    mix.js('resources/js/app.js', 'public/js')
        .extract(['vue'])

`extract` メソッドは、`vendor.js` ファイルに抽出するすべてのライブラリまたはモジュールの配列を受け入れます。上記のスニペットを例として使用すると、Mix は次のファイルを生成します。

<div class="content-list" markdown="1">

- `public/js/manifest.js`: *Webpack マニフェスト ランタイム*
- `public/js/vendor.js`: *ベンダー ライブラリ*
- `public/js/app.js`: *アプリケーション コード*

</div>

JavaScript エラーを回避するには、次のファイルを正しい順序でロードしてください。

    <script src="/js/manifest.js"></script>
    <script src="/js/vendor.js"></script>
    <script src="/js/app.js"></script>

<a name="custom-webpack-configuration"></a>
### カスタム Webpack 構成

場合によっては、基礎となる Webpack 構成を手動で変更する必要がある場合があります。たとえば、参照する必要がある特別なローダーまたはプラグインがある場合があります。

Mix は、短い Webpack 構成オーバーライドをマージできる便利な `webpackConfig` メソッドを提供します。これは、`webpack.config.js` ファイルの独自のコピーをコピーして管理する必要がないため、特に魅力的です。 `webpackConfig` メソッドはオブジェクトを受け入れます。このオブジェクトには、適用する [Webpack 固有の構成](https://webpack.js.org/configuration/) が含まれている必要があります。

    mix.webpackConfig({
        resolve: {
            modules: [
                path.resolve(__dirname, 'vendor/laravel/spark/resources/assets/js')
            ]
        }
    });

<a name="versioning-and-cache-busting"></a>
## バージョニング/キャッシュバスティング (Versioning / Cache Busting)

多くの開発者は、コンパイルされたアセットの末尾にタイムスタンプまたは一意のトークンを付けて、コードの古いコピーを提供するのではなく、ブラウザーに新しいアセットを強制的にロードさせます。 Mix は、`version` メソッドを使用してこれを自動的に処理できます。

`version` メソッドは、コンパイルされたすべてのファイルのファイル名に一意のハッシュを追加し、より便利なキャッシュ無効化を可能にします。

    mix.js('resources/js/app.js', 'public/js')
        .version();

バージョン管理されたファイルを生成した後は、正確なファイル名はわかりません。したがって、適切にハッシュされたアセットをロードするには、[views](/docs/{{version}}/views) 内で Laravel のグローバル `mix` 関数を使用する必要があります。 `mix` 関数は、ハッシュされたファイルの現在の名前を自動的に決定します。

    <script src="{{ mix('/js/app.js') }}"></script>

バージョン管理されたファイルは通常、開発では不要であるため、`npm run prod` 中にのみ実行するようにバージョン管理プロセスを指示できます。

    mix.js('resources/js/app.js', 'public/js');

    if (mix.inProduction()) {
        mix.version();
    }

<a name="custom-mix-base-urls"></a>
#### カスタム Mix ベース URL

Mix でコンパイルされたアセットがアプリケーションとは別の CDN にデプロイされている場合は、`mix` 関数によって生成されたベース URL を変更する必要があります。これを行うには、アプリケーションの `config/app.php` 構成ファイルに `mix_url` 構成オプションを追加します。

    'mix_url' => env('MIX_ASSET_URL', null)

Mix URL を構成した後、`mix` 関数は、アセットへの URL を生成するときに、構成された URL にプレフィックスを付けます。

```bash
https://cdn.example.com/js/app.js?id=1964becbdd96414518cd
```

<a name="browsersync-reloading"></a>
## ブラウザ同期のリロード (Browsersync Reloading)

[BrowserSync](https://browsersync.io/) は、ファイルの変更を自動的に監視し、手動で更新することなく変更をブラウザに挿入できます。 `mix.browserSync()` メソッドを呼び出すことで、これのサポートを有効にすることができます。

```js
mix.browserSync('laravel.test');
```

[BrowserSync オプション](https://browsersync.io/docs/options) は、JavaScript オブジェクトを `browserSync` メソッドに渡すことで指定できます。

```js
mix.browserSync({
    proxy: 'laravel.test'
});
```

次に、`npm run watch` コマンドを使用して webpack の開発サーバーを起動します。スクリプトまたは PHP ファイルを変更すると、ブラウザが即座にページを更新して変更を反映するのを確認できるようになりました。

<a name="environment-variables"></a>
## 環境変数 (Environment Variables)

`.env` ファイル内の環境変数の 1 つに `MIX_` というプレフィックスを付けることで、環境変数を `webpack.mix.js` スクリプトに挿入できます。

    MIX_SENTRY_DSN_PUBLIC=http://example.com

変数が `.env` ファイルで定義されたら、`process.env` オブジェクトを介して変数にアクセスできます。ただし、タスクの実行中に環境変数の値が変更された場合は、タスクを再起動する必要があります。

    process.env.MIX_SENTRY_DSN_PUBLIC

<a name="notifications"></a>
## 通知 (Notifications)

利用可能な場合、Mix はコンパイル時に OS 通知を自動的に表示し、コンパイルが成功したかどうかについて即座にフィードバックを提供します。ただし、これらの通知を無効にした方がよい場合もあります。そのような例の 1 つは、運用サーバー上で Mix をトリガーすることです。通知は、`disableNotifications` メソッドを使用して非アクティブ化できます。

    mix.disableNotifications();


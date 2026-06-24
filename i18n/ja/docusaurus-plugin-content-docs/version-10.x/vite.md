<!-- # Asset Bundling (Vite) -->
# Asset Bundling (Vite)

- [Introduction](#introduction)
- [Installation & Setup](#installation)
  - [Installing Node](#installing-node)
  - [Installing Vite and the Laravel Plugin](#installing-vite-and-laravel-plugin)
  - [Configuring Vite](#configuring-vite)
  - [Loading Your Scripts and Styles](#loading-your-scripts-and-styles)
- [Running Vite](#running-vite)
- [Working With JavaScript](#working-with-scripts)
  - [Aliases](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL Processing](#url-processing)
- [Working With Stylesheets](#working-with-stylesheets)
- [Working With Blade and Routes](#working-with-blade-and-routes)
  - [Processing Static Assets With Vite](#blade-processing-static-assets)
  - [Refreshing on Save](#blade-refreshing-on-save)
  - [Aliases](#blade-aliases)
- [Custom Base URLs](#custom-base-urls)
- [Environment Variables](#environment-variables)
- [Disabling Vite in Tests](#disabling-vite-in-tests)
- [Server-Side Rendering (SSR)](#ssr)
- [Script and Style Tag Attributes](#script-and-style-attributes)
  - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  - [Subresource Integrity (SRI)](#subresource-integrity-sri)
  - [Arbitrary Attributes](#arbitrary-attributes)
- [Advanced Customization](#advanced-customization)
  - [Correcting Dev Server URLs](#correcting-dev-server-urls)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Vite](https://vitejs.dev) is a modern frontend build tool that provides an extremely fast development environment and bundles your code for production. When building applications with Laravel, you will typically use Vite to bundle your application's CSS and JavaScript files into production ready assets. -->
[Vite](https://vitejs.dev) は、非常に高速な開発環境を提供し、実稼働用のコードをバンドルする最新のフロントエンド ビルド ツールです。 Laravel でアプリケーションを構築する場合、通常は Vite を使用して、アプリケーションの CSS ファイルと JavaScript ファイルを本番環境に対応したアセットにバンドルします。

<!-- Laravel integrates seamlessly with Vite by providing an official plugin and Blade directive to load your assets for development and production. -->
Laravel は、開発および本番用にアセットをロードするための公式プラグインと Blade ディレクティブを提供することで、Vite とシームレスに統合します。

> [!NOTE]
> Laravel Mix を実行していますか? Vite は、新しい Laravel インストールで Laravel Mix を置き換えました。 Mix のドキュメントについては、[Laravel Mix](https://laravel-mix.com/) Web サイトをご覧ください。 Vite に切り替えたい場合は、[migration guide](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite) をご覧ください。

<a name="vite-or-mix"></a>
<!-- #### Choosing Between Vite and Laravel Mix -->
#### Choosing Between Vite and Laravel Mix

<!-- Before transitioning to Vite, new Laravel applications utilized [Mix](https://laravel-mix.com/), which is powered by [webpack](https://webpack.js.org/), when bundling assets. Vite focuses on providing a faster and more productive experience when building rich JavaScript applications. If you are developing a Single Page Application (SPA), including those developed with tools like [Inertia](https://inertiajs.com), Vite will be the perfect fit. -->
Vite に移行する前、新しい Laravel アプリケーションは、アセットをバンドルするときに [Mix](https://laravel-mix.com/) を利用する [webpack](https://webpack.js.org/) を利用していました。 Vite は、リッチな JavaScript アプリケーションを構築する際に、より高速で生産性の高いエクスペリエンスを提供することに重点を置いています。 [Inertia](https://inertiajs.com) などのツールで開発されたものを含め、シングル ページ アプリケーション (SPA) を開発している場合は、Vite が最適です。

<!-- Vite also works well with traditional server-side rendered applications with JavaScript "sprinkles", including those using [Livewire](https://livewire.laravel.com). However, it lacks some features that Laravel Mix supports, such as the ability to copy arbitrary assets into the build that are not referenced directly in your JavaScript application. -->
Vite は、[Livewire](https://livewire.laravel.com) を使用するアプリケーションなど、JavaScript の「スプリンクル」を使用した従来のサーバーサイドでレンダリングされたアプリケーションでも適切に動作します。ただし、JavaScript アプリケーションで直接参照されない任意のアセットをビルドにコピーする機能など、Laravel Mix がサポートするいくつかの機能が欠けています。

<a name="migrating-back-to-mix"></a>
<!-- #### Migrating Back to Mix -->
#### Migrating Back to Mix

<!-- Have you started a new Laravel application using our Vite scaffolding but need to move back to Laravel Mix and webpack? No problem. Please consult our [official guide on migrating from Vite to Mix](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix). -->
Vite スキャフォールディングを使用して新しい Laravel アプリケーションを開始しましたが、Laravel Mix と webpack に戻る必要がありますか?問題ない。 [official guide on migrating from Vite to Mix](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix) にご相談ください。

<a name="installation"></a>
<!-- ## Installation & Setup -->
## Installation & Setup

> [!NOTE]
> 次のドキュメントでは、Laravel Vite プラグインを手動でインストールして構成する方法について説明します。ただし、Laravel の [starter kits](/docs/10.x/starter-kits) にはこのスキャフォールディングがすべて含まれており、Laravel と Vite を始めるための最速の方法です。

<a name="installing-node"></a>
<!-- ### Installing Node -->
### Installing Node

<!-- You must ensure that Node.js (16+) and NPM are installed before running Vite and the Laravel plugin: -->
Vite と Laravel プラグインを実行する前に、Node.js (16+) と NPM がインストールされていることを確認する必要があります。

```sh
node -v
npm -v
```

<!-- You can easily install the latest version of Node and NPM using simple graphical installers from [the official Node website](https://nodejs.org/en/download/). Or, if you are using [Laravel Sail](https://laravel.com/docs/10.x/sail), you may invoke Node and NPM through Sail: -->
[the official Node website](https://nodejs.org/en/download/) のシンプルなグラフィカル インストーラーを使用して、Node と NPM の最新バージョンを簡単にインストールできます。または、[Laravel Sail](https://laravel.com/docs/10.x/sail) を使用している場合は、Sail を通じて Node と NPM を呼び出すことができます。

```sh
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
<!-- ### Installing Vite and the Laravel Plugin -->
### Installing Vite and the Laravel Plugin

<!-- Within a fresh installation of Laravel, you will find a `package.json` file in the root of your application's directory structure. The default `package.json` file already includes everything you need to get started using Vite and the Laravel plugin. You may install your application's frontend dependencies via NPM: -->
Laravel を新規インストールすると、アプリケーションのディレクトリ構造のルートに `package.json` ファイルが見つかります。デフォルトの `package.json` ファイルには、Vite と Laravel プラグインの使用を開始するために必要なものがすべて含まれています。 NPM 経由でアプリケーションのフロントエンド依存関係をインストールできます。

```sh
npm install
```

<a name="configuring-vite"></a>
<!-- ### Configuring Vite -->
### Configuring Vite

<!-- Vite is configured via a `vite.config.js` file in the root of your project. You are free to customize this file based on your needs, and you may also install any other plugins your application requires, such as `@vitejs/plugin-vue` or `@vitejs/plugin-react`. -->
Vite は、プロジェクトのルートにある `vite.config.js` ファイルを介して設定されます。このファイルはニーズに基づいて自由にカスタマイズでき、アプリケーションに必要な他のプラグイン (`@vitejs/plugin-vue` や `@vitejs/plugin-react` など) をインストールすることもできます。

<!-- The Laravel Vite plugin requires you to specify the entry points for your application. These may be JavaScript or CSS files, and include preprocessed languages such as TypeScript, JSX, TSX, and Sass. -->
Laravel Vite プラグインでは、アプリケーションのエントリ ポイントを指定する必要があります。これらは JavaScript または CSS ファイルであり、TypeScript、JSX、TSX、Sass などの前処理された言語が含まれます。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css',
            'resources/js/app.js',
        ]),
    ],
});
```

<!-- If you are building an SPA, including applications built using Inertia, Vite works best without CSS entry points: -->
Inertia を使用して構築されたアプリケーションを含む SPA を構築している場合、Vite は CSS エントリ ポイントなしで最適に動作します。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css', // [tl! remove]
            'resources/js/app.js',
        ]),
    ],
});
```

<!-- Instead, you should import your CSS via JavaScript. Typically, this would be done in your application's `resources/js/app.js` file: -->
代わりに、JavaScript 経由で CSS をインポートする必要があります。通常、これはアプリケーションの `resources/js/app.js` ファイルで行われます。

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

<!-- The Laravel plugin also supports multiple entry points and advanced configuration options such as [SSR entry points](#ssr). -->
Laravel プラグインは、複数のエントリ ポイントと [SSR entry points](#ssr) などの高度な構成オプションもサポートしています。

<a name="working-with-a-secure-development-server"></a>
<!-- #### Working With a Secure Development Server -->
#### Working With a Secure Development Server

<!-- If your local development web server is serving your application via HTTPS, you may run into issues connecting to the Vite development server. -->
ローカル開発 Web サーバーが HTTPS 経由でアプリケーションを提供している場合、Vite 開発サーバーへの接続で問題が発生する可能性があります。

<!-- If you are using [Laravel Herd](https://herd.laravel.com) and have secured the site or you are using [Laravel Valet](/docs/10.x/valet) and have run the [secure command](/docs/10.x/valet#securing-sites) against your application, the Laravel Vite plugin will automatically detect and use the generated TLS certificate for you. -->
[Laravel Herd](https://herd.laravel.com) を使用していてサイトを保護している場合、または [Laravel Valet](/docs/10.x/valet) を使用していてアプリケーションに対して [secure command](/docs/10.x/valet#securing-sites) を実行している場合、Laravel Vite プラグインは生成された TLS 証明書を自動的に検出して使用します。

<!-- If you secured the site using a host that does not match the application's directory name, you may manually specify the host in your application's `vite.config.js` file: -->
アプリケーションのディレクトリ名と一致しないホストを使用してサイトを保護した場合は、アプリケーションの `vite.config.js` ファイルでホストを手動で指定できます。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            detectTls: 'my-app.test', // [tl! add]
        }),
    ],
});
```

<!-- When using another web server, you should generate a trusted certificate and manually configure Vite to use the generated certificates: -->
別の Web サーバーを使用する場合は、信頼できる証明書を生成し、生成された証明書を使用するように Vite を手動で設定する必要があります。

```js
// ...
import fs from 'fs'; // [tl! add]

const host = 'my-app.test'; // [tl! add]

export default defineConfig({
    // ...
    server: { // [tl! add]
        host, // [tl! add]
        hmr: { host }, // [tl! add]
        https: { // [tl! add]
            key: fs.readFileSync(`/path/to/${host}.key`), // [tl! add]
            cert: fs.readFileSync(`/path/to/${host}.crt`), // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<!-- If you are unable to generate a trusted certificate for your system, you may install and configure the [`@vitejs/plugin-basic-ssl` plugin](https://github.com/vitejs/vite-plugin-basic-ssl). When using untrusted certificates, you will need to accept the certificate warning for Vite's development server in your browser by following the "Local" link in your console when running the `npm run dev` command. -->
システムの信頼できる証明書を生成できない場合は、[`@vitejs/plugin-basic-ssl` plugin](https://github.com/vitejs/vite-plugin-basic-ssl) をインストールして構成できます。信頼できない証明書を使用する場合は、`npm run dev` コマンドの実行時にコンソールの「ローカル」リンクをクリックして、ブラウザーで Vite 開発サーバーに対する証明書の警告を受け入れる必要があります。

<a name="configuring-hmr-in-sail-on-wsl2"></a>
<!-- #### Running the Development Server in Sail on WSL2 -->
#### Running the Development Server in Sail on WSL2

<!-- When running the Vite development server within [Laravel Sail](/docs/10.x/sail) on Windows Subsystem for Linux 2 (WSL2), you should add the following configuration to your `vite.config.js` file to ensure the browser can communicate with the development server: -->
Windows Subsystem for Linux 2 (WSL2) 上の [Laravel Sail](/docs/10.x/sail) 内で Vite 開発サーバーを実行する場合は、ブラウザが開発サーバーと通信できるように、次の構成を `vite.config.js` ファイルに追加する必要があります。

```js
// ...

export default defineConfig({
    // ...
    server: { // [tl! add:start]
        hmr: {
            host: 'localhost',
        },
    }, // [tl! add:end]
});
```

<!-- If your file changes are not being reflected in the browser while the development server is running, you may also need to configure Vite's [`server.watch.usePolling` option](https://vitejs.dev/config/server-options.html#server-watch). -->
開発サーバーの実行中にファイルの変更がブラウザに反映されない場合は、Vite の [`server.watch.usePolling` option](https://vitejs.dev/config/server-options.html#server-watch) の設定も必要になる場合があります。

<a name="loading-your-scripts-and-styles"></a>
<!-- ### Loading Your Scripts and Styles -->
### Loading Your Scripts and Styles

<!-- With your Vite entry points configured, you may now reference them in a `@vite()` Blade directive that you add to the `<head>` of your application's root template: -->
Vite エントリ ポイントを設定したら、アプリケーションのルート テンプレートの `<head>` に追加する `@vite()` Blade ディレクティブでエントリ ポイントを参照できるようになります。

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

<!-- If you're importing your CSS via JavaScript, you only need to include the JavaScript entry point: -->
JavaScript 経由で CSS をインポートする場合、含める必要があるのは JavaScript エントリ ポイントのみです。

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

<!-- The `@vite` directive will automatically detect the Vite development server and inject the Vite client to enable Hot Module Replacement. In build mode, the directive will load your compiled and versioned assets, including any imported CSS. -->
`@vite` ディレクティブは、Vite 開発サーバーを自動的に検出し、Vite クライアントを挿入してホット モジュール交換を有効にします。ビルド モードでは、ディレクティブは、インポートされた CSS を含む、コンパイルおよびバージョン管理されたアセットを読み込みます。

<!-- If needed, you may also specify the build path of your compiled assets when invoking the `@vite` directive: -->
必要に応じて、`@vite` ディレクティブを呼び出すときに、コンパイルされたアセットのビルド パスを指定することもできます。

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
<!-- #### Inline Assets -->
#### Inline Assets

<!-- Sometimes it may be necessary to include the raw content of assets rather than linking to the versioned URL of the asset. For example, you may need to include asset content directly into your page when passing HTML content to a PDF generator. You may output the content of Vite assets using the `content` method provided by the `Vite` facade: -->
場合によっては、アセットのバージョン管理された URL にリンクするのではなく、アセットの生のコンテンツを含める必要がある場合があります。たとえば、HTML コンテンツを PDF ジェネレーターに渡すときに、アセット コンテンツをページに直接含める必要がある場合があります。 `Vite` ファサードによって提供される `content` メソッドを使用して、Vite アセットのコンテンツを出力できます。

```blade
@php
use Illuminate\Support\Facades\Vite;
@endphp

<!doctype html>
<head>
    {{-- ... --}}

    <style>
        {!! Vite::content('resources/css/app.css') !!}
    </style>
    <script>
        {!! Vite::content('resources/js/app.js') !!}
    </script>
</head>
```

<a name="running-vite"></a>
<!-- ## Running Vite -->
## Running Vite

<!-- There are two ways you can run Vite. You may run the development server via the `dev` command, which is useful while developing locally. The development server will automatically detect changes to your files and instantly reflect them in any open browser windows. -->
Vite を実行するには 2 つの方法があります。 `dev` コマンドを使用して開発サーバーを実行できます。これは、ローカルで開発する場合に便利です。開発サーバーはファイルへの変更を自動的に検出し、開いているブラウザ ウィンドウに即座に変更を反映します。

<!-- Or, running the `build` command will version and bundle your application's assets and get them ready for you to deploy to production: -->
または、`build` コマンドを実行すると、アプリケーションのアセットがバージョン管理されてバンドルされ、運用環境にデプロイできるようになります。

```shell
# Run the Vite development server...
npm run dev

# Build and version the assets for production...
npm run build
```

<!-- If you are running the development server in [Sail](/docs/10.x/sail) on WSL2, you may need some [additional configuration](#configuring-hmr-in-sail-on-wsl2) options. -->
WSL2 上の [Sail](/docs/10.x/sail) で開発サーバーを実行している場合は、いくつかの [additional configuration](#configuring-hmr-in-sail-on-wsl2) オプションが必要になる場合があります。

<a name="working-with-scripts"></a>
<!-- ## Working With JavaScript -->
## Working With JavaScript

<a name="aliases"></a>
<!-- ### Aliases -->
### Aliases

<!-- By default, The Laravel plugin provides a common alias to help you hit the ground running and conveniently import your application's assets: -->
デフォルトでは、Laravel プラグインは、すぐに作業を開始し、アプリケーションのアセットを簡単にインポートできるようにするための共通のエイリアスを提供します。

```js
{
    '@' => '/resources/js'
}
```

<!-- You may overwrite the `'@'` alias by adding your own to the `vite.config.js` configuration file: -->
独自のエイリアスを `vite.config.js` 構成ファイルに追加することで、`'@'` エイリアスを上書きできます。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel(['resources/ts/app.tsx']),
    ],
    resolve: {
        alias: {
            '@': '/resources/ts',
        },
    },
});
```

<a name="vue"></a>
<!-- ### Vue -->
### Vue

<!-- If you would like to build your frontend using the [Vue](https://vuejs.org/) framework, then you will also need to install the `@vitejs/plugin-vue` plugin: -->
[Vue](https://vuejs.org/) フレームワークを使用してフロントエンドを構築したい場合は、`@vitejs/plugin-vue` プラグインもインストールする必要があります。

```sh
npm install --save-dev @vitejs/plugin-vue
```

<!-- You may then include the plugin in your `vite.config.js` configuration file. There are a few additional options you will need when using the Vue plugin with Laravel: -->
その後、`vite.config.js` 構成ファイルにプラグインを含めることができます。 Laravel で Vue プラグインを使用する場合、必要となる追加オプションがいくつかあります。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.js']),
        vue({
            template: {
                transformAssetUrls: {
                    // The Vue plugin will re-write asset URLs, when referenced
                    // in Single File Components, to point to the Laravel web
                    // server. Setting this to `null` allows the Laravel plugin
                    // to instead re-write asset URLs to point to the Vite
                    // server instead.
                    base: null,

                    // The Vue plugin will parse absolute URLs and treat them
                    // as absolute paths to files on disk. Setting this to
                    // `false` will leave absolute URLs un-touched so they can
                    // reference assets in the public directory as expected.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]
> Laravel の [starter kits](/docs/10.x/starter-kits) には、適切な Laravel、Vue、および Vite 構成がすでに含まれています。 Laravel、Vue、Vite を始める最速の方法については、[Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia) をチェックしてください。

<a name="react"></a>
<!-- ### React -->
### React

<!-- If you would like to build your frontend using the [React](https://reactjs.org/) framework, then you will also need to install the `@vitejs/plugin-react` plugin: -->
[React](https://reactjs.org/) フレームワークを使用してフロントエンドを構築したい場合は、`@vitejs/plugin-react` プラグインもインストールする必要があります。

```sh
npm install --save-dev @vitejs/plugin-react
```

<!-- You may then include the plugin in your `vite.config.js` configuration file: -->
次に、`vite.config.js` 構成ファイルにプラグインを含めることができます。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.jsx']),
        react(),
    ],
});
```

<!-- You will need to ensure that any files containing JSX have a `.jsx` or `.tsx` extension, remembering to update your entry point, if required, as [shown above](#configuring-vite). -->
JSX を含むすべてのファイルに `.jsx` または `.tsx` 拡張子が付いていることを確認する必要があります。必要に応じて、エントリ ポイントを [shown above](#configuring-vite) として更新することを忘れないでください。

<!-- You will also need to include the additional `@viteReactRefresh` Blade directive alongside your existing `@vite` directive. -->
既存の `@vite` ディレクティブと一緒に、追加の `@viteReactRefresh` Blade ディレクティブを含める必要もあります。

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

<!-- The `@viteReactRefresh` directive must be called before the `@vite` directive. -->
`@viteReactRefresh` ディレクティブは、`@vite` ディレクティブの前に呼び出す必要があります。

> [!NOTE]
> Laravel の [starter kits](/docs/10.x/starter-kits) には、適切な Laravel、React、および Vite 構成がすでに含まれています。 Laravel、React、Vite を最も早く始める方法については、[Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia) をチェックしてください。

<a name="inertia"></a>
<!-- ### Inertia -->
### Inertia

<!-- The Laravel Vite plugin provides a convenient `resolvePageComponent` function to help you resolve your Inertia page components. Below is an example of the helper in use with Vue 3; however, you may also utilize the function in other frameworks such as React: -->
Laravel Vite プラグインは、Inertia ページコンポーネントの解決に役立つ便利な `resolvePageComponent` 関数を提供します。以下は、Vue 3 で使用されるヘルパの例です。ただし、この関数は React などの他のフレームワークでも利用できます。

```js
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
  resolve: (name) => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),
  setup({ el, App, props, plugin }) {
    return createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
});
```

> [!NOTE]
> Laravel の [starter kits](/docs/10.x/starter-kits) には、適切な Laravel、Inertia、および Vite 構成がすでに含まれています。 Laravel、Inertia、Vite を最速で始める方法については、[Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia) をチェックしてください。

<a name="url-processing"></a>
<!-- ### URL Processing -->
### URL Processing

<!-- When using Vite and referencing assets in your application's HTML, CSS, or JS, there are a couple of caveats to consider. First, if you reference assets with an absolute path, Vite will not include the asset in the build; therefore, you should ensure that the asset is available in your public directory. -->
Vite を使用し、アプリケーションの HTML、CSS、または JS でアセットを参照する場合、考慮すべき注意事項がいくつかあります。まず、絶対パスでアセットを参照すると、Vite はビルドにアセットを含めません。したがって、アセットがパブリック ディレクトリで利用可能であることを確認する必要があります。

<!-- When referencing relative asset paths, you should remember that the paths are relative to the file where they are referenced. Any assets referenced via a relative path will be re-written, versioned, and bundled by Vite. -->
相対アセット パスを参照する場合、パスは参照先のファイルからの相対パスであることに注意してください。相対パス経由で参照されるアセットはすべて、Vite によって書き換えられ、バージョン管理され、バンドルされます。

<!-- Consider the following project structure: -->
次のプロジェクト構造を考えてみましょう。

```nothing
public/
  taylor.png
resources/
  js/
    Pages/
      Welcome.vue
  images/
    abigail.png
```

<!-- The following example demonstrates how Vite will treat relative and absolute URLs: -->
次の例は、Vite が相対 URL と絶対 URL をどのように扱うかを示しています。

```html
<!-- This asset is not handled by Vite and will not be included in the build -->
<img src="/taylor.png">

<!-- This asset will be re-written, versioned, and bundled by Vite -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
<!-- ## Working With Stylesheets -->
## Working With Stylesheets

<!-- You can learn more about Vite's CSS support within the [Vite documentation](https://vitejs.dev/guide/features.html#css). If you are using PostCSS plugins such as [Tailwind](https://tailwindcss.com), you may create a `postcss.config.js` file in the root of your project and Vite will automatically apply it: -->
Vite の CSS サポートについて詳しくは、[Vite documentation](https://vitejs.dev/guide/features.html#css) をご覧ください。 [Tailwind](https://tailwindcss.com) などの PostCSS プラグインを使用している場合は、プロジェクトのルートに `postcss.config.js` ファイルを作成すると、Vite がそれを自動的に適用します。

```js
export default {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
```

> [!NOTE]
> Laravel の [starter kits](/docs/10.x/starter-kits) には、適切な Tailwind、PostCSS、および Vite 構成がすでに含まれています。または、スターター キットを使用せずに Tailwind と Laravel を使用したい場合は、[Tailwind's installation guide for Laravel](https://tailwindcss.com/docs/guides/laravel) をチェックしてください。

<a name="working-with-blade-and-routes"></a>
<!-- ## Working With Blade and Routes -->
## Working With Blade and Routes

<a name="blade-processing-static-assets"></a>
<!-- ### Processing Static Assets With Vite -->
### Processing Static Assets With Vite

<!-- When referencing assets in your JavaScript or CSS, Vite automatically processes and versions them. In addition, when building Blade based applications, Vite can also process and version static assets that you reference solely in Blade templates. -->
JavaScript または CSS でアセットを参照すると、Vite はそれらを自動的に処理してバージョン付けします。さらに、Blade ベースのアプリケーションを構築する場合、Vite は Blade テンプレート内でのみ参照する静的アセットを処理およびバージョン管理することもできます。

<!-- However, in order to accomplish this, you need to make Vite aware of your assets by importing the static assets into the application's entry point. For example, if you want to process and version all images stored in `resources/images` and all fonts stored in `resources/fonts`, you should add the following in your application's `resources/js/app.js` entry point: -->
ただし、これを実現するには、静的アセットをアプリケーションのエントリ ポイントにインポートして、Vite にアセットを認識させる必要があります。たとえば、`resources/images` に保存されているすべての画像と `resources/fonts` に保存されているすべてのフォントを処理してバージョン管理する場合は、アプリケーションの `resources/js/app.js` エントリ ポイントに次の行を追加する必要があります。

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

<!-- These assets will now be processed by Vite when running `npm run build`. You can then reference these assets in Blade templates using the `Vite::asset` method, which will return the versioned URL for a given asset: -->
これらのアセットは、`npm run build` の実行時に Vite によって処理されるようになります。その後、`Vite::asset` メソッドを使用してBlade テンプレートでこれらのアセットを参照できます。これにより、特定のアセットのバージョン管理された URL が返されます。

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

<a name="blade-refreshing-on-save"></a>
<!-- ### Refreshing on Save -->
### Refreshing on Save

<!-- When your application is built using traditional server-side rendering with Blade, Vite can improve your development workflow by automatically refreshing the browser when you make changes to view files in your application. To get started, you can simply specify the `refresh` option as `true`. -->
Blade を使用した従来のサーバー側レンダリングを使用してアプリケーションが構築されている場合、Vite はアプリケーション内のファイルを表示するために変更を加えたときにブラウザを自動的に更新することで、開発ワークフローを改善できます。まず、`refresh` オプションを `true` として指定するだけです。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: true,
        }),
    ],
});
```

<!-- When the `refresh` option is `true`, saving files in the following directories will trigger the browser to perform a full page refresh while you are running `npm run dev`: -->
`refresh` オプションが `true` の場合、次のディレクトリにファイルを保存すると、`npm run dev` の実行中にブラウザがページ全体の更新を実行します。

<!--
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`
-->
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

<!-- Watching the `routes/**` directory is useful if you are utilizing [Ziggy](https://github.com/tighten/ziggy) to generate route links within your application's frontend. -->
`routes/**` ディレクトリを監視すると、アプリケーションのフロントエンド内でルート リンクを生成するために [Ziggy](https://github.com/tighten/ziggy) を利用している場合に役立ちます。

<!-- If these default paths do not suit your needs, you can specify your own list of paths to watch: -->
これらのデフォルトのパスがニーズに合わない場合は、監視するパスの独自のリストを指定できます。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: ['resources/views/**'],
        }),
    ],
});
```

<!-- Under the hood, the Laravel Vite plugin uses the [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload) package, which offers some advanced configuration options to fine-tune this feature's behavior. If you need this level of customization, you may provide a `config` definition: -->
Laravel Vite プラグインは内部で [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload) パッケージを使用し、この機能の動作を微調整するための高度な構成オプションを提供します。このレベルのカスタマイズが必要な場合は、`config` 定義を指定できます。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: [{
                paths: ['path/to/watch/**'],
                config: { delay: 300 }
            }],
        }),
    ],
});
```

<a name="blade-aliases"></a>
<!-- ### Aliases -->
### Aliases

<!-- It is common in JavaScript applications to [create aliases](#aliases) to regularly referenced directories. But, you may also create aliases to use in Blade by using the `macro` method on the `Illuminate\Support\Facades\Vite` class. Typically, "macros" should be defined within the `boot` method of a [service provider](/docs/10.x/providers): -->
JavaScript アプリケーションでは、定期的に参照されるディレクトリに対して [create aliases](#aliases) を行うのが一般的です。ただし、`Illuminate\Support\Facades\Vite` クラスの `macro` メソッドを使用して、Blade で使用するエイリアスを作成することもできます。通常、「マクロ」は [service provider](/docs/10.x/providers) の `boot` メソッド内で定義する必要があります。

```
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

<!-- Once a macro has been defined, it can be invoked within your templates. For example, we can use the `image` macro defined above to reference an asset located at `resources/images/logo.png`: -->
マクロを定義すると、テンプレート内でマクロを呼び出すことができます。たとえば、上で定義した `image` マクロを使用して、`resources/images/logo.png` にあるアセットを参照できます。

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="custom-base-urls"></a>
<!-- ## Custom Base URLs -->
## Custom Base URLs

<!-- If your Vite compiled assets are deployed to a domain separate from your application, such as via a CDN, you must specify the `ASSET_URL` environment variable within your application's `.env` file: -->
Vite コンパイル済みアセットが CDN 経由など、アプリケーションとは別のドメインにデプロイされている場合は、アプリケーションの `.env` ファイル内で `ASSET_URL` 環境変数を指定する必要があります。

```env
ASSET_URL=https://cdn.example.com
```

<!-- After configuring the asset URL, all re-written URLs to your assets will be prefixed with the configured value: -->
アセット URL を構成すると、アセットへのすべての書き換えられた URL には、構成された値がプレフィックスとして付加されます。

```nothing
https://cdn.example.com/build/assets/app.9dce8d17.js
```

<!-- Remember that [absolute URLs are not re-written by Vite](#url-processing), so they will not be prefixed. -->
[absolute URLs are not re-written by Vite](#url-processing) であるため、プレフィックスは付けられないことに注意してください。

<a name="environment-variables"></a>
<!-- ## Environment Variables -->
## Environment Variables

<!-- You may inject environment variables into your JavaScript by prefixing them with `VITE_` in your application's `.env` file: -->
アプリケーションの `.env` ファイル内で環境変数に `VITE_` というプレフィックスを付けることで、JavaScript に環境変数を挿入できます。

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

<!-- You may access injected environment variables via the `import.meta.env` object: -->
挿入された環境変数には、`import.meta.env` オブジェクト経由でアクセスできます。

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
<!-- ## Disabling Vite in Tests -->
## Disabling Vite in Tests

<!-- Laravel's Vite integration will attempt to resolve your assets while running your tests, which requires you to either run the Vite development server or build your assets. -->
Laravel の Vite 統合では、テストの実行中にアセットの解決が試行されるため、Vite 開発サーバーを実行するか、アセットを構築する必要があります。

<!-- If you would prefer to mock Vite during testing, you may call the `withoutVite` method, which is available for any tests that extend Laravel's `TestCase` class: -->
テスト中に Vite をモックしたい場合は、Laravel の `TestCase` クラスを拡張するあらゆるテストで使用できる `withoutVite` メソッドを呼び出すことができます。

```php
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_vite_example(): void
    {
        $this->withoutVite();

        // ...
    }
}
```

<!-- If you would like to disable Vite for all tests, you may call the `withoutVite` method from the `setUp` method on your base `TestCase` class: -->
すべてのテストで Vite を無効にしたい場合は、基本 `TestCase` クラスの `setUp` メソッドから `withoutVite` メソッドを呼び出すことができます。

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutVite();
    }// [tl! add:end]
}
```

<a name="ssr"></a>
<!-- ## Server-Side Rendering (SSR) -->
## Server-Side Rendering (SSR)

<!-- The Laravel Vite plugin makes it painless to set up server-side rendering with Vite. To get started, create an SSR entry point at `resources/js/ssr.js` and specify the entry point by passing a configuration option to the Laravel plugin: -->
Laravel Vite プラグインを使用すると、Vite でのサーバー側レンダリングのセットアップが簡単になります。まず、`resources/js/ssr.js` で SSR エントリ ポイントを作成し、構成オプションを Laravel プラグインに渡してエントリ ポイントを指定します。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            ssr: 'resources/js/ssr.js',
        }),
    ],
});
```

<!-- To ensure you don't forget to rebuild the SSR entry point, we recommend augmenting the "build" script in your application's `package.json` to create your SSR build: -->
SSR エントリ ポイントの再構築を忘れないようにするために、アプリケーションの `package.json` の「ビルド」スクリプトを拡張して SSR ビルドを作成することをお勧めします。

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

<!-- Then, to build and start the SSR server, you may run the following commands: -->
次に、SSR サーバーを構築して起動するには、次のコマンドを実行します。

```sh
npm run build
node bootstrap/ssr/ssr.js
```

<!-- If you are using [SSR with Inertia](https://inertiajs.com/server-side-rendering), you may instead use the `inertia:start-ssr` Artisan command to start the SSR server: -->
[SSR with Inertia](https://inertiajs.com/server-side-rendering) を使用している場合は、代わりに `inertia:start-ssr` Artisan コマンドを使用して SSR サーバーを起動できます。

```sh
php artisan inertia:start-ssr
```

> [!NOTE]
> Laravel の [starter kits](/docs/10.x/starter-kits) には、適切な Laravel、Inertia SSR、および Vite 構成がすでに含まれています。 Laravel、Inertia SSR、Vite を始める最速の方法については、[Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia) をチェックしてください。

<a name="script-and-style-attributes"></a>
<!-- ## Script and Style Tag Attributes -->
## Script and Style Tag Attributes

<a name="content-security-policy-csp-nonce"></a>
<!-- ### Content Security Policy (CSP) Nonce -->
### Content Security Policy (CSP) Nonce

<!-- If you wish to include a [`nonce` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) on your script and style tags as part of your [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), you may generate or specify a nonce using the `useCspNonce` method within a custom [middleware](/docs/10.x/middleware): -->
スクリプトとスタイル タグに [`nonce` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) の一部として [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) を含めたい場合は、カスタム [middleware](/docs/10.x/middleware) 内で `useCspNonce` メソッドを使用してノンスを生成または指定できます。

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Vite;
use Symfony\Component\HttpFoundation\Response;

class AddContentSecurityPolicyHeaders
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        Vite::useCspNonce();

        return $next($request)->withHeaders([
            'Content-Security-Policy' => "script-src 'nonce-".Vite::cspNonce()."'",
        ]);
    }
}
```

<!-- After invoking the `useCspNonce` method, Laravel will automatically include the `nonce` attributes on all generated script and style tags. -->
`useCspNonce` メソッドを呼び出した後、Laravel は生成されたすべてのスクリプトタグとスタイルタグに `nonce` 属性を自動的に含めます。

<!-- If you need to specify the nonce elsewhere, including the [Ziggy `@route` directive](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) included with Laravel's [starter kits](/docs/10.x/starter-kits), you may retrieve it using the `cspNonce` method: -->
Laravel の [Ziggy `@route` directive](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) に含まれる [starter kits](/docs/10.x/starter-kits) など、他の場所で nonce を指定する必要がある場合は、 `cspNonce` メソッドを使用して取得できます。

```blade
@routes(nonce: Vite::cspNonce())
```

<!-- If you already have a nonce that you would like to instruct Laravel to use, you may pass the nonce to the `useCspNonce` method: -->
Laravel に使用するように指示したい nonce がすでにある場合は、その nonce を `useCspNonce` メソッドに渡すことができます。

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
<!-- ### Subresource Integrity (SRI) -->
### Subresource Integrity (SRI)

<!-- If your Vite manifest includes `integrity` hashes for your assets, Laravel will automatically add the `integrity` attribute on any script and style tags it generates in order to enforce [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity). By default, Vite does not include the `integrity` hash in its manifest, but you may enable it by installing the [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM plugin: -->
Vite マニフェストにアセットの `integrity` ハッシュが含まれている場合、Laravel は [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) を強制するために、生成するスクリプトとスタイル タグに `integrity` 属性を自動的に追加します。デフォルトでは、Vite のマニフェストには `integrity` ハッシュが含まれていませんが、[`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM プラグインをインストールすることで有効にすることができます。

```shell
npm install --save-dev vite-plugin-manifest-sri
```

<!-- You may then enable this plugin in your `vite.config.js` file: -->
その後、`vite.config.js` ファイルでこのプラグインを有効にすることができます。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import manifestSRI from 'vite-plugin-manifest-sri';// [tl! add]

export default defineConfig({
    plugins: [
        laravel({
            // ...
        }),
        manifestSRI(),// [tl! add]
    ],
});
```

<!-- If required, you may also customize the manifest key where the integrity hash can be found: -->
必要に応じて、整合性ハッシュが見つかるマニフェスト キーをカスタマイズすることもできます。

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

<!-- If you would like to disable this auto-detection completely, you may pass `false` to the `useIntegrityKey` method: -->
この自動検出を完全に無効にしたい場合は、`false` を `useIntegrityKey` メソッドに渡します。

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
<!-- ### Arbitrary Attributes -->
### Arbitrary Attributes

<!-- If you need to include additional attributes on your script and style tags, such as the [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) attribute, you may specify them via the `useScriptTagAttributes` and `useStyleTagAttributes` methods. Typically, this methods should be invoked from a [service provider](/docs/10.x/providers): -->
スクリプトおよびスタイル タグに [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 属性などの追加の属性を含める必要がある場合は、`useScriptTagAttributes` および `useStyleTagAttributes` メソッドを使用して指定できます。通常、このメソッドは [service provider](/docs/10.x/providers) から呼び出す必要があります。

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // Specify a value for the attribute...
    'async' => true, // Specify an attribute without a value...
    'integrity' => false, // Exclude an attribute that would otherwise be included...
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

<!-- If you need to conditionally add attributes, you may pass a callback that will receive the asset source path, its URL, its manifest chunk, and the entire manifest: -->
条件付きで属性を追加する必要がある場合は、アセットのソース パス、その URL、そのマニフェスト チャンク、およびマニフェスト全体を受け取るコールバックを渡すことができます。

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $src === 'resources/js/app.js' ? 'reload' : false,
]);

Vite::useStyleTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $chunk && $chunk['isEntry'] ? 'reload' : false,
]);
```

> [!WARNING]
> Vite 開発サーバーの実行中、`$chunk` および `$manifest` 引数は `null` になります。

<a name="advanced-customization"></a>
<!-- ## Advanced Customization -->
## Advanced Customization

<!-- Out of the box, Laravel's Vite plugin uses sensible conventions that should work for the majority of applications; however, sometimes you may need to customize Vite's behavior. To enable additional customization options, we offer the following methods and options which can be used in place of the `@vite` Blade directive: -->
Laravel の Vite プラグインは、そのままの状態で、ほとんどのアプリケーションで機能する賢明な規則を使用しています。ただし、Vite の動作をカスタマイズする必要がある場合があります。追加のカスタマイズ オプションを有効にするために、`@vite` Blade ディレクティブの代わりに使用できる次のメソッドとオプションが提供されています。

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // Customize the "hot" file...
            ->useBuildDirectory('bundle') // Customize the build directory...
            ->useManifestFilename('assets.json') // Customize the manifest filename...
            ->withEntryPoints(['resources/js/app.js']) // Specify the entry points...
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // Customize the backend path generation for built assets...
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

<!-- Within the `vite.config.js` file, you should then specify the same configuration: -->
`vite.config.js` ファイル内で、同じ構成を指定する必要があります。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // Customize the "hot" file...
            buildDirectory: 'bundle', // Customize the build directory...
            input: ['resources/js/app.js'], // Specify the entry points...
        }),
    ],
    build: {
      manifest: 'assets.json', // Customize the manifest filename...
    },
});
```

<a name="correcting-dev-server-urls"></a>
<!-- ### Correcting Dev Server URLs -->
### Correcting Dev Server URLs

<!-- Some plugins within the Vite ecosystem assume that URLs which begin with a forward-slash will always point to the Vite dev server. However, due to the nature of the Laravel integration, this is not the case. -->
Vite エコシステム内の一部のプラグインは、スラッシュで始まる URL が常に Vite dev サーバーを指すことを前提としています。ただし、Laravel 統合の性質により、これは当てはまりません。

<!-- For example, the `vite-imagetools` plugin outputs URLs like the following while Vite is serving your assets: -->
たとえば、`vite-imagetools` プラグインは、Vite がアセットを提供しているときに次のような URL を出力します。

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

<!-- The `vite-imagetools` plugin is expecting that the output URL will be intercepted by Vite and the plugin may then handle all URLs that start with `/@imagetools`. If you are using plugins that are expecting this behaviour, you will need to manually correct the URLs. You can do this in your `vite.config.js` file by using the `transformOnServe` option. -->
`vite-imagetools` プラグインは、出力 URL が Vite によってインターセプトされることを予期しており、プラグインは `/@imagetools` で始まるすべての URL を処理する可能性があります。この動作を想定しているプラ​​グインを使用している場合は、URL を手動で修正する必要があります。これは、`transformOnServe` オプションを使用して、`vite.config.js` ファイルで行うことができます。

<!-- In this particular example, we will prepend the dev server URL to all occurrences of `/@imagetools` within the generated code: -->
この特定の例では、生成されたコード内のすべての `/@imagetools` の先頭に開発サーバー URL を追加します。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { imagetools } from 'vite-imagetools';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            transformOnServe: (code, devServerUrl) => code.replaceAll('/@imagetools', devServerUrl+'/@imagetools'),
        }),
        imagetools(),
    ],
});
```

<!-- Now, while Vite is serving Assets, it will output URLs that point to the Vite dev server: -->
これで、Vite がアセットを提供している間、Vite 開発サーバーを指す URL が出力されます。

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```


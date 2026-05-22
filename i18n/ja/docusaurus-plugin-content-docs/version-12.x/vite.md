# アセットバンドル (Vite) (Asset Bundling (Vite))

- [Introduction](#introduction)
- [インストールとセットアップ](#installation)
  - [ノードのインストール](#installing-node)
  - [Vite と Laravel プラグインのインストール](#installing-vite-and-laravel-plugin)
  - [Viteの設定](#configuring-vite)
  - [スクリプトとスタイルをロードする](#loading-your-scripts-and-styles)
- [ランニングバイト](#running-vite)
- [JavaScript の操作](#working-with-scripts)
  - [Aliases](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Svelte](#svelte)
  - [Inertia](#inertia)
  - [URL処理](#url-processing)
- [スタイルシートの操作](#working-with-stylesheets)
- [Bladeとルートの操作](#working-with-blade-and-routes)
  - [Vite を使用した静的アセットの処理](#blade-processing-static-assets)
  - [保存時に更新中](#blade-refreshing-on-save)
  - [Aliases](#blade-aliases)
- [アセットのプリフェッチ](#asset-prefetching)
- [カスタムベースURL](#custom-base-urls)
- [環境変数](#environment-variables)
- [テストでの Vite の無効化](#disabling-vite-in-tests)
- [サーバーサイド レンダリング (SSR)](#ssr)
- [スクリプトおよびスタイルタグの属性](#script-and-style-attributes)
  - [コンテンツ セキュリティ ポリシー (CSP) ナンス](#content-security-policy-csp-nonce)
  - [サブリソースの整合性 (SRI)](#subresource-integrity-sri)
  - [任意の属性](#arbitrary-attributes)
- [高度なカスタマイズ](#advanced-customization)
  - [開発サーバーのクロスオリジンリソース共有 (CORS)](#cors)
  - [開発サーバーの URL の修正](#correcting-dev-server-urls)

<a name="introduction"></a>
## 導入 (Introduction)

[Vite](https://vitejs.dev) は、非常に高速な開発環境を提供し、実稼働用のコードをバンドルする最新のフロントエンド ビルド ツールです。 Laravel でアプリケーションを構築する場合、通常は Vite を使用して、アプリケーションの CSS ファイルと JavaScript ファイルを実稼働可能なアセットにバンドルします。

Laravel は、開発および本番用にアセットをロードするための公式プラグインと Blade ディレクティブを提供することで、Vite とシームレスに統合します。

<a name="installation"></a>
## インストールとセットアップ (Installation & Setup)

> [!NOTE]
> 次のドキュメントでは、Laravel Vite プラグインを手動でインストールして構成する方法について説明します。ただし、Laravel の [スターターキット](/docs/{{version}}/starter-kits) にはこのスキャフォールディングがすべて含まれており、Laravel と Vite を始めるための最速の方法です。

<a name="installing-node"></a>
### ノードのインストール

Vite と Laravel プラグインを実行する前に、Node.js (16+) と NPM がインストールされていることを確認する必要があります。

```shell
node -v
npm -v
```

[ノードの公式ウェブサイト](https://nodejs.org/en/download/) のシンプルなグラフィカル インストーラーを使用して、Node と NPM の最新バージョンを簡単にインストールできます。または、[Laravel Sail](https://laravel.com/docs/{{version}}/sail) を使用している場合は、Sail を通じて Node と NPM を呼び出すことができます。

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite と Laravel プラグインのインストール

Laravel を新規インストールすると、アプリケーションのディレクトリ構造のルートに `package.json` ファイルが見つかります。デフォルトの `package.json` ファイルには、Vite と Laravel プラグインの使用を開始するために必要なものがすべて含まれています。 NPM 経由でアプリケーションのフロントエンド依存関係をインストールできます。

```shell
npm install
```

<a name="configuring-vite"></a>
### Viteの設定

Vite は、プロジェクトのルートにある `vite.config.js` ファイルを介して設定されます。このファイルはニーズに基づいて自由にカスタマイズでき、アプリケーションに必要な他のプラグイン (`@vitejs/plugin-react`、`@sveltejs/vite-plugin-svelte`、`@vitejs/plugin-vue` など) をインストールすることもできます。

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

代わりに、JavaScript 経由で CSS をインポートする必要があります。通常、これはアプリケーションの `resources/js/app.js` ファイルで行われます。

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel プラグインは、複数のエントリ ポイントと [SSRエントリーポイント](#ssr) などの高度な構成オプションもサポートしています。

<a name="working-with-a-secure-development-server"></a>
#### 安全な開発サーバーの使用

ローカル開発 Web サーバーが HTTPS 経由でアプリケーションを提供している場合、Vite 開発サーバーへの接続で問題が発生する可能性があります。

[LaravelのHerd](https://herd.laravel.com) を使用していてサイトを保護している場合、または [Laravel Valet](/docs/{{version}}/valet) を使用していてアプリケーションに対して [安全なコマンド](/docs/{{version}}/valet#securing-sites) を実行している場合、Laravel Vite プラグインは生成された TLS 証明書を自動的に検出して使用します。

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

システムの信頼できる証明書を生成できない場合は、[@vitejs/plugin-basic-ssl プラグイン](https://github.com/vitejs/vite-plugin-basic-ssl) をインストールして構成できます。信頼できない証明書を使用する場合は、`npm run dev` コマンドの実行時にコンソールの「ローカル」リンクをクリックして、ブラウザーで Vite 開発サーバーに対する証明書の警告を受け入れる必要があります。

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2 上の Sail で開発サーバーを実行する

Windows Subsystem for Linux 2 (WSL2) 上の [Laravel Sail](/docs/{{version}}/sail) 内で Vite 開発サーバーを実行する場合は、ブラウザが開発サーバーと通信できるように、次の構成を `vite.config.js` ファイルに追加する必要があります。

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

開発サーバーの実行中にファイルの変更がブラウザに反映されない場合は、Vite の [server.watch.usePolling オプション](https://vitejs.dev/config/server-options.html#server-watch) の設定も必要になる場合があります。

<a name="loading-your-scripts-and-styles"></a>
### スクリプトとスタイルをロードする

Vite エントリ ポイントを設定したら、アプリケーションのルート テンプレートの `<head>` に追加する `@vite()` Blade ディレクティブでエントリ ポイントを参照できるようになります。

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

JavaScript 経由で CSS をインポートする場合、含める必要があるのは JavaScript エントリ ポイントのみです。

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` ディレクティブは、Vite 開発サーバーを自動的に検出し、Vite クライアントを挿入してホット モジュール交換を有効にします。ビルド モードでは、ディレクティブは、インポートされた CSS を含む、コンパイルおよびバージョン管理されたアセットを読み込みます。

必要に応じて、`@vite` ディレクティブを呼び出すときに、コンパイルされたアセットのビルド パスを指定することもできます。

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### インラインアセット

場合によっては、アセットのバージョン管理された URL にリンクするのではなく、アセットの生のコンテンツを含める必要がある場合があります。たとえば、HTML コンテンツを PDF ジェネレーターに渡すときに、アセット コンテンツをページに直接含める必要がある場合があります。 `Vite` ファサードによって提供される `content` メソッドを使用して、Vite アセットのコンテンツを出力できます。

```blade
@use('Illuminate\Support\Facades\Vite')

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
## ランニングバイト (Running Vite)

Vite を実行するには 2 つの方法があります。 `dev` コマンドを使用して開発サーバーを実行できます。これは、ローカルで開発する場合に便利です。開発サーバーはファイルへの変更を自動的に検出し、開いているブラウザ ウィンドウに即座に変更を反映します。

または、`build` コマンドを実行すると、アプリケーションのアセットがバージョン管理されてバンドルされ、運用環境にデプロイできるようになります。

```shell
# Run the Vite development server...
npm run dev

# Build and version the assets for production...
npm run build
```

WSL2 上の [Sail](/docs/{{version}}/sail) で開発サーバーを実行している場合は、いくつかの [追加構成](#configuring-hmr-in-sail-on-wsl2) オプションが必要になる場合があります。

<a name="working-with-scripts"></a>
## JavaScript の操作 (Working With JavaScript)

<a name="aliases"></a>
### 別名

デフォルトでは、Laravel プラグインは、すぐに作業を開始し、アプリケーションのアセットを簡単にインポートできるようにするための共通のエイリアスを提供します。

```js
{
    '@' => '/resources/js'
}
```

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
### ヴュー

[Vue](https://vuejs.org/) フレームワークを使用してフロントエンドを構築したい場合は、`@vitejs/plugin-vue` プラグインもインストールする必要があります。

```shell
npm install --save-dev @vitejs/plugin-vue
```

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
> Laravel の [スターターキット](/docs/{{version}}/starter-kits) には、適切な Laravel、Vue、および Vite 構成がすでに含まれています。これらのスターター キットは、Laravel、Vue、および Vite を始めるための最速の方法を提供します。

<a name="react"></a>
### 反応する

[React](https://reactjs.org/) フレームワークを使用してフロントエンドを構築したい場合は、`@vitejs/plugin-react` プラグインもインストールする必要があります。

```shell
npm install --save-dev @vitejs/plugin-react
```

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

JSX を含むすべてのファイルに `.jsx` または `.tsx` 拡張子が付いていることを確認する必要があります。必要に応じて、エントリ ポイントを [上に示した](#configuring-vite) として更新することを忘れないでください。

既存の `@vite` ディレクティブと一緒に、追加の `@viteReactRefresh` Blade ディレクティブを含める必要もあります。

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh` ディレクティブは、`@vite` ディレクティブの前に呼び出す必要があります。

> [!NOTE]
> Laravel の [スターターキット](/docs/{{version}}/starter-kits) には、適切な Laravel、React、および Vite 構成がすでに含まれています。これらのスターター キットは、Laravel、React、および Vite を始めるための最速の方法を提供します。

<a name="svelte"></a>
### スレンダー

[Svelte](https://svelte.dev/) フレームワークを使用してフロントエンドを構築したい場合は、`@sveltejs/vite-plugin-svelte` プラグインもインストールする必要があります。

```shell
npm install --save-dev @sveltejs/vite-plugin-svelte
```

その後、`vite.config.js` 構成ファイルにプラグインを含めることができます。

```js
import { svelte } from '@sveltejs/vite-plugin-svelte';
import laravel from 'laravel-vite-plugin';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    laravel({
      input: ['resources/js/app.ts'],
      ssr: 'resources/js/ssr.ts',
      refresh: true,
    }),
    svelte(),
  ],
});
```

> [!NOTE]
> Laravel の [スターターキット](/docs/{{version}}/starter-kits) には、適切な Laravel、Svelte、および Vite 構成がすでに含まれています。これらのスターター キットは、Laravel、Svelte、および Vite を始めるための最速の方法を提供します。

<a name="inertia"></a>
### Inertia

Laravel Vite プラグインは、Inertia ページコンポーネントの解決に役立つ便利な `resolvePageComponent` 関数を提供します。以下は、Vue 3 で使用されるヘルパの例です。ただし、この関数は React や Svelte などの他のフレームワークでも利用できます。

```js
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
  resolve: (name) => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
});
```

Vite のコード分割機能を Inertia で使用している場合は、[アセットのプリフェッチ](#asset-prefetching) を設定することをお勧めします。

> [!NOTE]
> Laravel の [スターターキット](/docs/{{version}}/starter-kits) には、適切な Laravel、Inertia、および Vite 構成がすでに含まれています。これらのスターター キットは、Laravel、Inertia、および Vite を始めるための最速の方法を提供します。

<a name="url-processing"></a>
### URL処理

Vite を使用し、アプリケーションの HTML、CSS、または JS でアセットを参照する場合、考慮すべき注意事項がいくつかあります。まず、絶対パスでアセットを参照すると、Vite はビルドにアセットを含めません。したがって、アセットがパブリック ディレクトリで利用可能であることを確認する必要があります。 [専用の CSS エントリポイント](#configuring-vite) を使用する場合は、絶対パスの使用を避ける必要があります。これは、開発中にブラウザがパブリック ディレクトリからではなく、CSS がホストされている Vite 開発サーバーからこれらのパスをロードしようとするためです。

相対アセット パスを参照する場合、パスは参照先のファイルからの相対パスであることに注意してください。相対パス経由で参照されるアセットはすべて、Vite によって書き換えられ、バージョン管理され、バンドルされます。

次のプロジェクト構造を考えてみましょう。

```text
public/
  taylor.png
resources/
  js/
    Pages/
      Welcome.vue
  images/
    abigail.png
```

次の例は、Vite が相対 URL と絶対 URL をどのように扱うかを示しています。

```html
<!-- This asset is not handled by Vite and will not be included in the build -->
<img src="/taylor.png">

<!-- This asset will be re-written, versioned, and bundled by Vite -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
## スタイルシートの操作 (Working With Stylesheets)

> [!NOTE]
> Laravel の [スターターキット](/docs/{{version}}/starter-kits) には、適切な Tailwind と Vite 構成がすでに含まれています。または、スターター キットを使用せずに Tailwind と Laravel を使用したい場合は、[Tailwind の Laravel インストールガイド](https://tailwindcss.com/docs/guides/laravel) をチェックしてください。

すべての Laravel アプリケーションには、Tailwind と適切に構成された `vite.config.js` ファイルがすでに含まれています。したがって、Vite 開発サーバーを起動するか、Laravel 開発サーバーと Vite 開発サーバーの両方を起動する `dev` Composer コマンドを実行するだけで済みます。

```shell
composer run dev
```

アプリケーションの CSS は、`resources/css/app.css` ファイル内に配置される場合があります。

<a name="working-with-blade-and-routes"></a>
## Bladeとルートの操作 (Working With Blade and Routes)

<a name="blade-processing-static-assets"></a>
### Vite を使用した静的アセットの処理

JavaScript または CSS でアセットを参照すると、Vite はそれらを自動的に処理してバージョン付けします。さらに、Blade ベースのアプリケーションを構築する場合、Vite は Blade テンプレート内でのみ参照する静的アセットを処理およびバージョン管理することもできます。

ただし、これを実現するには、静的アセットをアプリケーションのエントリ ポイントにインポートして、Vite にアセットを認識させる必要があります。たとえば、`resources/images` に保存されているすべての画像と `resources/fonts` に保存されているすべてのフォントを処理してバージョン管理する場合は、アプリケーションの `resources/js/app.js` エントリ ポイントに次の行を追加する必要があります。

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

これらのアセットは、`npm run build` の実行時に Vite によって処理されるようになります。その後、`Vite::asset` メソッドを使用してBlade テンプレートでこれらのアセットを参照できます。これにより、特定のアセットのバージョン管理された URL が返されます。

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

<a name="blade-refreshing-on-save"></a>
### 保存時に更新中

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

`refresh` オプションが `true` の場合、次のディレクトリにファイルを保存すると、`npm run dev` の実行中にブラウザがページ全体の更新を実行します。

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

`routes/**` ディレクトリを監視すると、アプリケーションのフロントエンド内でルート リンクを生成するために [Ziggy](https://github.com/tighten/ziggy) を利用している場合に役立ちます。

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

Laravel Vite プラグインは内部で [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload) パッケージを使用し、この機能の動作を微調整するための高度な構成オプションを提供します。このレベルのカスタマイズが必要な場合は、`config` 定義を指定できます。

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
### 別名

JavaScript アプリケーションでは、定期的に参照されるディレクトリに対して [エイリアスを作成する](#aliases) を行うのが一般的です。ただし、`Illuminate\Support\Facades\Vite` クラスの `macro` メソッドを使用して、Blade で使用するエイリアスを作成することもできます。通常、「マクロ」は [サービスプロバイダ](/docs/{{version}}/providers) の `boot` メソッド内で定義する必要があります。

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

マクロを定義すると、テンプレート内でマクロを呼び出すことができます。たとえば、上で定義した `image` マクロを使用して、`resources/images/logo.png` にあるアセットを参照できます。

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="asset-prefetching"></a>
## アセットのプリフェッチ (Asset Prefetching)

Vite のコード分割機能を使用して SPA を構築すると、必要なアセットが各ページ ナビゲーションでフェッチされます。この動作により、UI レンダリングの遅延が発生する可能性があります。これが、選択したフロントエンド フレームワークにとって問題である場合、Laravel は、最初のページ読み込み時にアプリケーションの JavaScript および CSS アセットを積極的にプリフェッチする機能を提供します。

[サービスプロバイダ](/docs/{{version}}/providers) の `boot` メソッドで `Vite::prefetch` メソッドを呼び出すことで、Laravel にアセットを積極的にプリフェッチするように指示できます。

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Vite;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Vite::prefetch(concurrency: 3);
    }
}
```

上の例では、ページの読み込みごとに最大 `3` の同時ダウンロードでアセットがプリフェッチされます。アプリケーションのニーズに合わせて同時実行数を変更したり、アプリケーションがすべてのアセットを一度にダウンロードする必要がある場合は同時実行数の制限を指定したりできません。

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

デフォルトでは、[ページ_load_イベント](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) が起動するとプリフェッチが開始されます。プリフェッチの開始時期をカスタマイズしたい場合は、Vite がリッスンするイベントを指定できます。

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

上記のコードを考慮すると、`window` オブジェクトで `vite:prefetch` イベントを手動で送出すると、プリフェッチが開始されます。たとえば、ページが読み込まれてから 3 秒後にプリフェッチを開始することができます。

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## カスタムベースURL (Custom Base URLs)

Vite コンパイル済みアセットが CDN 経由など、アプリケーションとは別のドメインにデプロイされている場合は、アプリケーションの `.env` ファイル内で `ASSET_URL` 環境変数を指定する必要があります。

```env
ASSET_URL=https://cdn.example.com
```

アセット URL を構成すると、アセットへのすべての書き換えられた URL には、構成された値がプレフィックスとして付加されます。

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[絶対 URL は Vite によって書き換えられません](#url-processing) であるため、プレフィックスは付けられないことに注意してください。

<a name="environment-variables"></a>
## 環境変数 (Environment Variables)

アプリケーションの `.env` ファイル内で環境変数に `VITE_` というプレフィックスを付けることで、JavaScript に環境変数を挿入できます。

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

挿入された環境変数には、`import.meta.env` オブジェクト経由でアクセスできます。

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## テストでの Vite の無効化 (Disabling Vite in Tests)

Laravel の Vite 統合では、テストの実行中にアセットの解決が試行されるため、Vite 開発サーバーを実行するか、アセットを構築する必要があります。

テスト中に Vite をモックしたい場合は、Laravel の `TestCase` クラスを拡張するあらゆるテストで使用できる `withoutVite` メソッドを呼び出すことができます。

```php tab=Pest
test('without vite example', function () {
    $this->withoutVite();

    // ...
});
```

```php tab=PHPUnit
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

すべてのテストで Vite を無効にしたい場合は、基本 `TestCase` クラスの `setUp` メソッドから `withoutVite` メソッドを呼び出すことができます。

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutVite();
    }// [tl! add:end]
}
```

<a name="ssr"></a>
## サーバーサイド レンダリング (SSR) (Server-Side Rendering (SSR))

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

SSR エントリ ポイントの再構築を忘れないようにするために、アプリケーションの `package.json` の「ビルド」スクリプトを拡張して SSR ビルドを作成することをお勧めします。

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

次に、SSR サーバーを構築して起動するには、次のコマンドを実行します。

```shell
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia付きSSR](https://inertiajs.com/server-side-rendering) を使用している場合は、代わりに `inertia:start-ssr` Artisan コマンドを使用して SSR サーバーを起動できます。

```shell
php artisan inertia:start-ssr
```

> [!NOTE]
> Laravel の [スターターキット](/docs/{{version}}/starter-kits) には、適切な Laravel、Inertia SSR、および Vite 構成がすでに含まれています。これらのスターター キットは、Laravel、Inertia SSR、および Vite を始めるための最速の方法を提供します。

<a name="script-and-style-attributes"></a>
## スクリプトおよびスタイルタグの属性 (Script and Style Tag Attributes)

<a name="content-security-policy-csp-nonce"></a>
### コンテンツ セキュリティ ポリシー (CSP) ナンス

[コンテンツセキュリティポリシー](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) の一部としてスクリプトとスタイル タグに [ノンス属性](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) を含めたい場合は、カスタム [middleware](/docs/{{version}}/middleware) 内で `useCspNonce` メソッドを使用してノンスを生成または指定できます。

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

`useCspNonce` メソッドを呼び出した後、Laravel は生成されたすべてのスクリプトタグとスタイルタグに `nonce` 属性を自動的に含めます。

Laravel の [スターターキット](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) に含まれる [Ziggy `@route` ディレクティブ](/docs/{{version}}/starter-kits) など、他の場所で nonce を指定する必要がある場合は、 `cspNonce` メソッドを使用して取得できます。

```blade
@routes(nonce: Vite::cspNonce())
```

Laravel に使用するように指示したい nonce がすでにある場合は、その nonce を `useCspNonce` メソッドに渡すことができます。

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### サブリソースの整合性 (SRI)

Vite マニフェストにアセットの `integrity` ハッシュが含まれている場合、Laravel は [サブリソースの整合性](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) を強制するために、生成するスクリプトとスタイル タグに `integrity` 属性を自動的に追加します。デフォルトでは、Vite のマニフェストには `integrity` ハッシュが含まれていませんが、[vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM プラグインをインストールすることで有効にすることができます。

```shell
npm install --save-dev vite-plugin-manifest-sri
```

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

必要に応じて、整合性ハッシュが見つかるマニフェスト キーをカスタマイズすることもできます。

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

この自動検出を完全に無効にしたい場合は、`false` を `useIntegrityKey` メソッドに渡します。

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 任意の属性

スクリプトおよびスタイル タグに [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 属性などの追加の属性を含める必要がある場合は、`useScriptTagAttributes` および `useStyleTagAttributes` メソッドを使用して指定できます。通常、このメソッドは [サービスプロバイダ](/docs/{{version}}/providers) から呼び出す必要があります。

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
## 高度なカスタマイズ (Advanced Customization)

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

<a name="cors"></a>
### 開発サーバーのクロスオリジンリソース共有 (CORS)

Vite 開発サーバーからアセットを取得しているときにブラウザでクロスオリジン リソース共有 (CORS) の問題が発生した場合は、開発サーバーへのカスタム オリジン アクセスを許可する必要がある場合があります。 Vite を Laravel プラグインと組み合わせると、追加の設定なしで次のオリジンが可能になります。

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- プロジェクトの `.env` 内の `APP_URL`

プロジェクトにカスタム オリジンを許可する最も簡単な方法は、アプリケーションの `APP_URL` 環境変数がブラウザでアクセスしているオリジンと一致していることを確認することです。たとえば、`https://my-app.laravel` にアクセスした場合は、次と一致するように `.env` を更新する必要があります。

```env
APP_URL=https://my-app.laravel
```

複数のオリジンのサポートなど、オリジンをさらにきめ細かく制御する必要がある場合は、[Vite の包括的かつ柔軟な組み込み CORS サーバー構成](https://vite.dev/config/server-options.html#server-cors) を使用する必要があります。たとえば、プロジェクトの `vite.config.js` ファイルの `server.cors.origin` 構成オプションで複数の起点を指定できます。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            refresh: true,
        }),
    ],
    server: {  // [tl! add]
        cors: {  // [tl! add]
            origin: [  // [tl! add]
                'https://backend.laravel',  // [tl! add]
                'http://admin.laravel:8566',  // [tl! add]
            ],  // [tl! add]
        },  // [tl! add]
    },  // [tl! add]
});
```

正規表現パターンを含めることもできます。これは、`*.laravel` など、特定のトップレベル ドメインのすべてのオリジンを許可する場合に役立ちます。

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            refresh: true,
        }),
    ],
    server: {  // [tl! add]
        cors: {  // [tl! add]
            origin: [ // [tl! add]
                // Supports: SCHEME://DOMAIN.laravel[:PORT] [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
### 開発サーバーの URL の修正

Vite エコシステム内の一部のプラグインは、スラッシュで始まる URL が常に Vite dev サーバーを指すことを前提としています。ただし、Laravel 統合の性質により、これは当てはまりません。

たとえば、`vite-imagetools` プラグインは、Vite がアセットを提供しているときに次のような URL を出力します。

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

`vite-imagetools` プラグインは、出力 URL が Vite によってインターセプトされることを予期しており、プラグインは `/@imagetools` で始まるすべての URL を処理する可能性があります。この動作を想定しているプラ​​グインを使用している場合は、URL を手動で修正する必要があります。これは、`transformOnServe` オプションを使用して、`vite.config.js` ファイルで行うことができます。

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

これで、Vite がアセットを提供している間、Vite 開発サーバーを指す URL が出力されます。

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```


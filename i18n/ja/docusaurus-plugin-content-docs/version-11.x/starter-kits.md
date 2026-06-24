<!-- # Starter Kits -->
# Starter Kits

- [Introduction](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
    - [Breeze and Blade](#breeze-and-blade)
    - [Breeze and Livewire](#breeze-and-livewire)
    - [Breeze and React / Vue](#breeze-and-inertia)
    - [Breeze and Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- To give you a head start building your new Laravel application, we are happy to offer authentication and application starter kits. These kits automatically scaffold your application with the routes, controllers, and views you need to register and authenticate your application's users. -->
新しい Laravel アプリケーションの構築をすぐに始められるように、認証およびアプリケーションのスターター キットを喜んで提供します。これらのキットは、アプリケーションのユーザーを登録および認証するために必要なルート、コントローラ、ビューを使用してアプリケーションを自動的にスキャフォールディングします。

<!-- While you are welcome to use these starter kits, they are not required. You are free to build your own application from the ground up by simply installing a fresh copy of Laravel. Either way, we know you will build something great! -->
これらのスターター キットを使用しても構いませんが、必須ではありません。 Laravel の新しいコピーをインストールするだけで、独自のアプリケーションを最初から自由に構築できます。いずれにせよ、私たちはあなたが素晴らしいものを作り上げることを確信しています。

<a name="laravel-breeze"></a>
<!-- ## Laravel Breeze -->
## Laravel Breeze

<!-- [Laravel Breeze](https://github.com/laravel/breeze) is a minimal, simple implementation of all of Laravel's [authentication features](/docs/11.x/authentication), including login, registration, password reset, email verification, and password confirmation. In addition, Breeze includes a simple "profile" page where the user may update their name, email address, and password. -->
[Laravel Breeze](https://github.com/laravel/breeze) は、ログイン、登録、パスワードのリセット、メール検証、パスワードの確認を含む、Laravel の [authentication features](/docs/11.x/authentication) のすべてを最小限にシンプルに実装したものです。さらに、Breeze には、ユーザーが自分の名前、電子メール アドレス、パスワードを更新できる簡単な「プロフィール」ページが含まれています。

<!-- Laravel Breeze's default view layer is made up of simple [Blade templates](/docs/11.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). Additionally, Breeze provides scaffolding options based on [Livewire](https://livewire.laravel.com) or [Inertia](https://inertiajs.com), with the choice of using Vue or React for the Inertia-based scaffolding. -->
Laravel Breezeのデフォルトのビューレイヤーは、[Blade templates](/docs/11.x/blade)でスタイル設定されたシンプルな[Tailwind CSS](https://tailwindcss.com)で構成されています。さらに、Breeze は、[Livewire](https://livewire.laravel.com) または [Inertia](https://inertiajs.com) に基づくスキャフォールディング オプションを提供し、Inertiaベースのスキャフォールディングに Vue または React を使用することを選択できます。

<!-- <img src="https://laravel.com/img/docs/breeze-register.png"/> -->
<img src="https://laravel.com/img/docs/breeze-register.png"/>

<!-- #### Laravel Bootcamp -->
#### Laravel Bootcamp

<!-- If you're new to Laravel, feel free to jump into the [Laravel Bootcamp](https://bootcamp.laravel.com). The Laravel Bootcamp will walk you through building your first Laravel application using Breeze. It's a great way to get a tour of everything that Laravel and Breeze have to offer. -->
Laravel を初めて使用する場合は、お気軽に [Laravel Bootcamp](https://bootcamp.laravel.com) にアクセスしてください。 Laravel Bootcamp では、Breeze を使用して最初の Laravel アプリケーションを構築する手順を説明します。これは、Laravel と Breeze が提供するすべての機能を見学するのに最適な方法です。

<a name="laravel-breeze-installation"></a>
<!-- ### Installation -->
### Installation

<!-- First, you should [create a new Laravel application](/docs/11.x/installation). If you create your application using the [Laravel installer](/docs/11.x/installation#creating-a-laravel-project), you will be prompted to install Laravel Breeze during the installation process. Otherwise, you will need to follow the manual installation instructions below. -->
まず、[create a new Laravel application](/docs/11.x/installation) を実行する必要があります。 [Laravel installer](/docs/11.x/installation#creating-a-laravel-project) を使用してアプリケーションを作成する場合、インストールプロセス中に Laravel Breeze をインストールするように求められます。それ以外の場合は、以下の手動インストール手順に従う必要があります。

<!-- If you have already created a new Laravel application without a starter kit, you may manually install Laravel Breeze using Composer: -->
スターターキットなしで新しい Laravel アプリケーションをすでに作成している場合は、Composer を使用して Laravel Breeze を手動でインストールできます。

```shell
composer require laravel/breeze --dev
```

<!-- After Composer has installed the Laravel Breeze package, you should run the `breeze:install` Artisan command. This command publishes the authentication views, routes, controllers, and other resources to your application. Laravel Breeze publishes all of its code to your application so that you have full control and visibility over its features and implementation. -->
Composer が Laravel Breeze パッケージをインストールした後、`breeze:install` Artisan コマンドを実行する必要があります。このコマンドは、認証ビュー、ルート、コントローラ、およびその他のリソースをアプリケーションに公開します。 Laravel Breeze はすべてのコードをアプリケーションに公開するため、その機能と実装を完全に制御し、可視化できます。

<!-- The `breeze:install` command will prompt you for your preferred frontend stack and testing framework: -->
`breeze:install` コマンドを実行すると、優先するフロントエンド スタックとテスト フレームワークを指定するよう求められます。

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<a name="breeze-and-blade"></a>
<!-- ### Breeze and Blade -->
### Breeze and Blade

<!-- The default Breeze "stack" is the Blade stack, which utilizes simple [Blade templates](/docs/11.x/blade) to render your application's frontend. The Blade stack may be installed by invoking the `breeze:install` command with no other additional arguments and selecting the Blade frontend stack. After Breeze's scaffolding is installed, you should also compile your application's frontend assets: -->
Breeze のデフォルトの「スタック」は Blade スタックで、単純な [Blade templates](/docs/11.x/blade) を利用してアプリケーションのフロントエンドをレンダリングします。Blade スタックは、他の追加の引数を指定せずに `breeze:install` コマンドを呼び出し、Blade フロントエンド スタックを選択することでインストールできます。 Breeze のスキャフォールディングがインストールされたら、アプリケーションのフロントエンド アセットもコンパイルする必要があります。

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<!-- Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file. -->
次に、Web ブラウザでアプリケーションの `/login` または `/register` URL に移動します。 Breeze のルートはすべて、`routes/auth.php` ファイル内で定義されます。

> [!NOTE]
> アプリケーションの CSS と JavaScript のコンパイルの詳細については、Laravel の [Vite documentation](/docs/11.x/vite#running-vite) を確認してください。

<a name="breeze-and-livewire"></a>
<!-- ### Breeze and Livewire -->
### Breeze and Livewire

<!-- Laravel Breeze also offers [Livewire](https://livewire.laravel.com) scaffolding. Livewire is a powerful way of building dynamic, reactive, front-end UIs using just PHP. -->
Laravel Breeze は [Livewire](https://livewire.laravel.com) 足場も提供しています。 Livewire は、PHP だけを使用して動的でリアクティブなフロントエンド UI を構築する強力な方法です。

<!-- Livewire is a great fit for teams that primarily use Blade templates and are looking for a simpler alternative to JavaScript-driven SPA frameworks like Vue and React. -->
Livewire は、主に Blade テンプレートを使用し、Vue や React などの JavaScript 駆動の SPA フレームワークのよりシンプルな代替手段を探しているチームに最適です。

<!-- To use the Livewire stack, you may select the Livewire frontend stack when executing the `breeze:install` Artisan command. After Breeze's scaffolding is installed, you should run your database migrations: -->
Livewire スタックを使用するには、`breeze:install` Artisan コマンドを実行するときに Livewire フロントエンド スタックを選択できます。 Breeze のスキャフォールディングがインストールされたら、データベースの移行を実行する必要があります。

```shell
php artisan breeze:install

php artisan migrate
```

<a name="breeze-and-inertia"></a>
<!-- ### Breeze and React / Vue -->
### Breeze and React / Vue

<!-- Laravel Breeze also offers React and Vue scaffolding via an [Inertia](https://inertiajs.com) frontend implementation. Inertia allows you to build modern, single-page React and Vue applications using classic server-side routing and controllers. -->
Laravel Breeze は、[Inertia](https://inertiajs.com) フロントエンド実装を介して React と Vue スキャフォールディングも提供します。 Inertia を使用すると、従来のサーバー側のルーティングとコントローラを使用して、最新の単一ページの React および Vue アプリケーションを構築できます。

<!-- Inertia lets you enjoy the frontend power of React and Vue combined with the incredible backend productivity of Laravel and lightning-fast [Vite](https://vitejs.dev) compilation. To use an Inertia stack, you may select the Vue or React frontend stacks when executing the `breeze:install` Artisan command. -->
Inertia を使用すると、React と Vue のフロントエンドのパワーを、Laravel の驚異的なバックエンドの生産性と超高速の [Vite](https://vitejs.dev) コンパイルと組み合わせて楽しむことができます。 Inertia スタックを使用するには、`breeze:install` Artisan コマンドの実行時に Vue または React フロントエンド スタックを選択できます。

<!-- When selecting the Vue or React frontend stack, the Breeze installer will also prompt you to determine if you would like [Inertia SSR](https://inertiajs.com/server-side-rendering) or TypeScript support. After Breeze's scaffolding is installed, you should also compile your application's frontend assets: -->
Vue または React フロントエンド スタックを選択すると、Breeze インストーラーによって、[Inertia SSR](https://inertiajs.com/server-side-rendering) または TypeScript のサポートを希望するかどうかを決定するよう求められます。 Breeze のスキャフォールディングがインストールされたら、アプリケーションのフロントエンド アセットもコンパイルする必要があります。

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<!-- Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file. -->
次に、Web ブラウザでアプリケーションの `/login` または `/register` URL に移動します。 Breeze のルートはすべて、`routes/auth.php` ファイル内で定義されます。

<a name="breeze-and-next"></a>
<!-- ### Breeze and Next.js / API -->
### Breeze and Next.js / API

<!-- Laravel Breeze can also scaffold an authentication API that is ready to authenticate modern JavaScript applications such as those powered by [Next](https://nextjs.org), [Nuxt](https://nuxt.com), and others. To get started, select the API stack as your desired stack when executing the `breeze:install` Artisan command: -->
Laravel Breeze は、[Next](https://nextjs.org)、[Nuxt](https://nuxt.com) などを利用した最新の JavaScript アプリケーションを認証する準備ができている認証 API をスキャフォールディングすることもできます。まず、`breeze:install` Artisan コマンドを実行するときに、目的のスタックとして API スタックを選択します。

```shell
php artisan breeze:install

php artisan migrate
```

<!-- During installation, Breeze will add a `FRONTEND_URL` environment variable to your application's `.env` file. This URL should be the URL of your JavaScript application. This will typically be `http://localhost:3000` during local development. In addition, you should ensure that your `APP_URL` is set to `http://localhost:8000`, which is the default URL used by the `serve` Artisan command. -->
インストール中に、Breeze は `FRONTEND_URL` 環境変数をアプリケーションの `.env` ファイルに追加します。この URL は、JavaScript アプリケーションの URL である必要があります。通常、ローカル開発中は `http://localhost:3000` になります。さらに、`APP_URL` が `http://localhost:8000` に設定されていることを確認する必要があります。これは、`serve` Artisan コマンドで使用されるデフォルトの URL です。

<a name="next-reference-implementation"></a>
<!-- #### Next.js Reference Implementation -->
#### Next.js Reference Implementation

<!-- Finally, you are ready to pair this backend with the frontend of your choice. A Next reference implementation of the Breeze frontend is [available on GitHub](https://github.com/laravel/breeze-next). This frontend is maintained by Laravel and contains the same user interface as the traditional Blade and Inertia stacks provided by Breeze. -->
最後に、このバックエンドを選択したフロントエンドと組み合わせる準備が整いました。 Breeze フロントエンドの次のリファレンス実装は、[available on GitHub](https://github.com/laravel/breeze-next) です。このフロントエンドは Laravel によって保守されており、Breeze によって提供される従来の Blade および Inertia スタックと同じユーザー インターフェイスが含まれています。

<a name="laravel-jetstream"></a>
<!-- ## Laravel Jetstream -->
## Laravel Jetstream

<!-- While Laravel Breeze provides a simple and minimal starting point for building a Laravel application, Jetstream augments that functionality with more robust features and additional frontend technology stacks. **For those brand new to Laravel, we recommend learning the ropes with Laravel Breeze before graduating to Laravel Jetstream.** -->
Laravel Breeze は Laravel アプリケーションを構築するためのシンプルかつ最小限の開始点を提供しますが、Jetstream はより堅牢な機能と追加のフロントエンド テクノロジ スタックでその機能を強化します。 **Laravel を初めて使用する方は、Laravel Jetstream を卒業する前に、Laravel Breeze でコツを学ぶことをお勧めします。**

<!-- Jetstream provides a beautifully designed application scaffolding for Laravel and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://livewire.laravel.com) or [Inertia](https://inertiajs.com) driven frontend scaffolding. -->
Jetstream は、Laravel 用に美しく設計されたアプリケーション スキャフォールディングを提供します。これには、ログイン、登録、電子メール検証、2 要素認証、セッション管理、Laravel Sanctum を介した API サポート、およびオプションのチーム管理が含まれます。 Jetstream は [Tailwind CSS](https://tailwindcss.com) を使用して設計されており、[Livewire](https://livewire.laravel.com) または [Inertia](https://inertiajs.com) 駆動のフロントエンド スキャフォールディングを選択できます。

<!-- Complete documentation for installing Laravel Jetstream can be found within the [official Jetstream documentation](https://jetstream.laravel.com). -->
Laravel Jetstream のインストールに関する完全なドキュメントは、[official Jetstream documentation](https://jetstream.laravel.com) 内にあります。


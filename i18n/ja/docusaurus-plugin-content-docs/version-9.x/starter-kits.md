<!-- # Starter Kits -->
# Starter Kits

- [Introduction](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
    - [Breeze & Blade](#breeze-and-blade)
    - [Breeze & React / Vue](#breeze-and-inertia)
    - [Breeze & Next.js / API](#breeze-and-next)
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

<!-- [Laravel Breeze](https://github.com/laravel/breeze) is a minimal, simple implementation of all of Laravel's [authentication features](/docs/9.x/authentication), including login, registration, password reset, email verification, and password confirmation. In addition, Breeze includes a simple "profile" page where the user may update their name, email address, and password. -->
[Laravel Breeze](https://github.com/laravel/breeze) は、ログイン、登録、パスワードのリセット、メール検証、パスワードの確認を含む、Laravel の [authentication features](/docs/9.x/authentication) のすべてを最小限にシンプルに実装したものです。さらに、Breeze には、ユーザーが自分の名前、電子メール アドレス、パスワードを更新できる簡単な「プロフィール」ページが含まれています。

<!-- Laravel Breeze's default view layer is made up of simple [Blade templates](/docs/9.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). Or, Breeze can scaffold your application using Vue or React and [Inertia](https://inertiajs.com). -->
Laravel Breezeのデフォルトのビューレイヤーは、[Blade templates](/docs/9.x/blade)でスタイル設定されたシンプルな[Tailwind CSS](https://tailwindcss.com)で構成されています。または、Breeze は、Vue または React と [Inertia](https://inertiajs.com) を使用してアプリケーションをスキャフォールディングできます。

<!-- Breeze provides a wonderful starting point for beginning a fresh Laravel application and is also a great choice for projects that plan to take their Blade templates to the next level with [Laravel Livewire](https://laravel-livewire.com). -->
Breeze は、新しい Laravel アプリケーションを開始するための素晴らしい出発点を提供し、[Laravel Livewire](https://laravel-livewire.com) を使用して Blade テンプレートを次のレベルに引き上げることを計画しているプロジェクトにも最適です。

<!-- <img src="https://laravel.com/img/docs/breeze-register.png"/> -->
<img src="https://laravel.com/img/docs/breeze-register.png"/>

<!-- #### Laravel Bootcamp -->
#### Laravel Bootcamp

<!-- If you're new to Laravel, feel free to jump into the [Laravel Bootcamp](https://bootcamp.laravel.com). The Laravel Bootcamp will walk you through building your first Laravel application using Breeze. It's a great way to get a tour of everything that Laravel and Breeze have to offer. -->
Laravel を初めて使用する場合は、お気軽に [Laravel Bootcamp](https://bootcamp.laravel.com) にアクセスしてください。 Laravel Bootcamp では、Breeze を使用して最初の Laravel アプリケーションを構築する手順を説明します。これは、Laravel と Breeze が提供するすべての機能を見学するのに最適な方法です。

<a name="laravel-breeze-installation"></a>
<!-- ### Installation -->
### Installation

<!-- First, you should [create a new Laravel application](/docs/9.x/installation), configure your database, and run your [database migrations](/docs/9.x/migrations). Once you have created a new Laravel application, you may install Laravel Breeze using Composer: -->
まず、[create a new Laravel application](/docs/9.x/installation) を実行し、データベースを構成し、[database migrations](/docs/9.x/migrations) を実行する必要があります。新しい Laravel アプリケーションを作成したら、Composer を使用して Laravel Breeze をインストールできます。

```shell
composer require laravel/breeze --dev
```

<!-- Once Breeze is installed, you may scaffold your application using one of the Breeze "stacks" discussed in the documentation below. -->
Breeze がインストールされたら、以下のドキュメントで説明されている Breeze の「スタック」の 1 つを使用してアプリケーションをスキャフォールディングできます。

<a name="breeze-and-blade"></a>
<!-- ### Breeze & Blade -->
### Breeze & Blade

<!-- After Composer has installed the Laravel Breeze package, you may run the `breeze:install` Artisan command. This command publishes the authentication views, routes, controllers, and other resources to your application. Laravel Breeze publishes all of its code to your application so that you have full control and visibility over its features and implementation. -->
Composer が Laravel Breeze パッケージをインストールした後、`breeze:install` Artisan コマンドを実行できます。このコマンドは、認証ビュー、ルート、コントローラ、およびその他のリソースをアプリケーションに公開します。 Laravel Breeze はすべてのコードをアプリケーションに公開するため、その機能と実装を完全に制御し、可視化できます。

<!-- The default Breeze "stack" is the Blade stack, which utilizes simple [Blade templates](/docs/9.x/blade) to render your application's frontend. The Blade stack may be installed by invoking the `breeze:install` command with no other additional arguments. After Breeze's scaffolding is installed, you should also compile your application's frontend assets: -->
Breeze のデフォルトの「スタック」は Blade スタックで、単純な [Blade templates](/docs/9.x/blade) を利用してアプリケーションのフロントエンドをレンダリングします。Blade スタックは、他の追加の引数を指定せずに `breeze:install` コマンドを呼び出すことによってインストールできます。 Breeze のスキャフォールディングがインストールされたら、アプリケーションのフロントエンド アセットもコンパイルする必要があります。

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<!-- Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file. -->
次に、Web ブラウザでアプリケーションの `/login` または `/register` URL に移動します。 Breeze のルートはすべて、`routes/auth.php` ファイル内で定義されます。

<a name="dark-mode"></a>
<!-- #### Dark Mode -->
#### Dark Mode

<!-- If you would like Breeze to include "dark mode" support when scaffolding your application's frontend, simply provide the `--dark` directive when executing the `breeze:install` command: -->
アプリケーションのフロントエンドをスキャフォールディングするときに Breeze に「ダーク モード」サポートを含めたい場合は、`breeze:install` コマンドを実行するときに `--dark` ディレクティブを指定するだけです。

```shell
php artisan breeze:install --dark
```

> [!NOTE]
> アプリケーションの CSS と JavaScript のコンパイルの詳細については、Laravel の [Vite documentation](/docs/9.x/vite#running-vite) を確認してください。

<a name="breeze-and-inertia"></a>
<!-- ### Breeze & React / Vue -->
### Breeze & React / Vue

<!-- Laravel Breeze also offers React and Vue scaffolding via an [Inertia](https://inertiajs.com) frontend implementation. Inertia allows you to build modern, single-page React and Vue applications using classic server-side routing and controllers. -->
Laravel Breeze は、[Inertia](https://inertiajs.com) フロントエンド実装を介して React と Vue スキャフォールディングも提供します。 Inertia を使用すると、従来のサーバー側のルーティングとコントローラを使用して、最新の単一ページの React および Vue アプリケーションを構築できます。

<!-- Inertia lets you enjoy the frontend power of React and Vue combined with the incredible backend productivity of Laravel and lightning-fast [Vite](https://vitejs.dev) compilation. To use an Inertia stack, specify `vue` or `react` as your desired stack when executing the `breeze:install` Artisan command. After Breeze's scaffolding is installed, you should also compile your application's frontend assets: -->
Inertia を使用すると、React と Vue のフロントエンドのパワーを、Laravel の驚異的なバックエンドの生産性と超高速の [Vite](https://vitejs.dev) コンパイルと組み合わせて楽しむことができます。 Inertia スタックを使用するには、`breeze:install` Artisan コマンドを実行するときに、希望のスタックとして `vue` または `react` を指定します。 Breeze のスキャフォールディングがインストールされたら、アプリケーションのフロントエンド アセットもコンパイルする必要があります。

```shell
php artisan breeze:install vue

# Or...

php artisan breeze:install react

php artisan migrate
npm install
npm run dev
```

<!-- Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file. -->
次に、Web ブラウザでアプリケーションの `/login` または `/register` URL に移動します。 Breeze のルートはすべて、`routes/auth.php` ファイル内で定義されます。

<a name="server-side-rendering"></a>
<!-- #### Server-Side Rendering -->
#### Server-Side Rendering

<!-- If you would like Breeze to scaffold support for [Inertia SSR](https://inertiajs.com/server-side-rendering), you may provide the `ssr` option when invoking the `breeze:install` command: -->
Breeze に [Inertia SSR](https://inertiajs.com/server-side-rendering) のサポートをスキャフォールディングさせたい場合は、`breeze:install` コマンドを呼び出すときに `ssr` オプションを指定できます。

```shell
php artisan breeze:install vue --ssr
php artisan breeze:install react --ssr
```

<a name="breeze-and-next"></a>
<!-- ### Breeze & Next.js / API -->
### Breeze & Next.js / API

<!-- Laravel Breeze can also scaffold an authentication API that is ready to authenticate modern JavaScript applications such as those powered by [Next](https://nextjs.org), [Nuxt](https://nuxt.com), and others. To get started, specify the `api` stack as your desired stack when executing the `breeze:install` Artisan command: -->
Laravel Breeze は、[Next](https://nextjs.org)、[Nuxt](https://nuxt.com) などを利用した最新の JavaScript アプリケーションを認証する準備ができている認証 API をスキャフォールディングすることもできます。まず、`breeze:install` Artisan コマンドを実行するときに、目的のスタックとして `api` スタックを指定します。

```shell
php artisan breeze:install api

php artisan migrate
```

<!-- During installation, Breeze will add a `FRONTEND_URL` environment variable to your application's `.env` file. This URL should be the URL of your JavaScript application. This will typically be `http://localhost:3000` during local development. In addition, you should ensure that your `APP_URL` is set to `http://localhost:8000`, which is the default URL used by the `serve` Artisan command. -->
インストール中に、Breeze は `FRONTEND_URL` 環境変数をアプリケーションの `.env` ファイルに追加します。この URL は、JavaScript アプリケーションの URL である必要があります。通常、ローカル開発中は `http://localhost:3000` になります。さらに、`APP_URL` が `http://localhost:8000` に設定されていることを確認する必要があります。これは、`serve` Artisan コマンドで使用されるデフォルトの URL です。

<a name="next-reference-implementation"></a>
<!-- #### Next.js Reference Implementation -->
#### Next.js Reference Implementation

<!-- Finally, you are ready to pair this backend with the frontend of your choice. A Next reference implementation of the Breeze frontend is [available on GitHub](https://github.com/laravel/breeze-next). This frontend is maintained by Laravel and contains the same user interface as the traditional Blade and Inertia stacks provided by Breeze. -->
最後に、このバックエンドを選択したフロントエンドと組み合わせる準備が整いました。 Breeze フロントエンドの Next リファレンス実装は、[available on GitHub](https://github.com/laravel/breeze-next) です。このフロントエンドは Laravel によって保守されており、Breeze によって提供される従来の Blade および Inertia スタックと同じユーザー インターフェイスが含まれています。

<a name="laravel-jetstream"></a>
<!-- ## Laravel Jetstream -->
## Laravel Jetstream

<!-- While Laravel Breeze provides a simple and minimal starting point for building a Laravel application, Jetstream augments that functionality with more robust features and additional frontend technology stacks. **For those brand new to Laravel, we recommend learning the ropes with Laravel Breeze before graduating to Laravel Jetstream.** -->
Laravel Breeze は Laravel アプリケーションを構築するためのシンプルかつ最小限の開始点を提供しますが、Jetstream はより堅牢な機能と追加のフロントエンド テクノロジ スタックでその機能を強化します。 **Laravel を初めて使用する方は、Laravel Jetstream を卒業する前に、Laravel Breeze でコツを学ぶことをお勧めします。**

<!-- Jetstream provides a beautifully designed application scaffolding for Laravel and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://laravel-livewire.com) or [Inertia](https://inertiajs.com) driven frontend scaffolding. -->
Jetstream は、Laravel 用に美しく設計されたアプリケーション スキャフォールディングを提供します。これには、ログイン、登録、電子メール検証、2 要素認証、セッション管理、Laravel Sanctum を介した API サポート、およびオプションのチーム管理が含まれます。 Jetstream は [Tailwind CSS](https://tailwindcss.com) を使用して設計されており、[Livewire](https://laravel-livewire.com) または [Inertia](https://inertiajs.com) 駆動のフロントエンド スキャフォールディングを選択できます。

<!-- Complete documentation for installing Laravel Jetstream can be found within the [official Jetstream documentation](https://jetstream.laravel.com/introduction.html). -->
Laravel Jetstream のインストールに関する完全なドキュメントは、[official Jetstream documentation](https://jetstream.laravel.com/introduction.html) 内にあります。


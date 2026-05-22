# スターターキット (Starter Kits)

- [Introduction](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
    - [Breezeと刃](#breeze-and-blade)
    - [BreezeとLivewire](#breeze-and-livewire)
    - [Breeze と React / Vue](#breeze-and-inertia)
    - [Breeze と Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## 導入 (Introduction)

新しい Laravel アプリケーションの構築をすぐに始められるように、認証およびアプリケーションのスターター キットを喜んで提供します。これらのキットは、アプリケーションのユーザーを登録および認証するために必要なルート、コントローラ、ビューを使用してアプリケーションを自動的にスキャフォールディングします。

これらのスターター キットを使用しても構いませんが、必須ではありません。 Laravel の新しいコピーをインストールするだけで、独自のアプリケーションを最初から自由に構築できます。いずれにせよ、私たちはあなたが素晴らしいものを作り上げることを確信しています。

<a name="laravel-breeze"></a>
## Laravel Breeze (Laravel Breeze)

[Laravel Breeze](https://github.com/laravel/breeze) は、ログイン、登録、パスワードのリセット、メール検証、パスワードの確認を含む、Laravel の [認証機能](/docs/{{version}}/authentication) のすべてを最小限にシンプルに実装したものです。さらに、Breeze には、ユーザーが自分の名前、電子メール アドレス、パスワードを更新できる簡単な「プロフィール」ページが含まれています。

Laravel Breezeのデフォルトのビューレイヤーは、[Tailwind CSS](/docs/{{version}}/blade)でスタイル設定されたシンプルな[Blade テンプレート](https://tailwindcss.com)で構成されています。さらに、Breeze は、[Livewire](https://livewire.laravel.com) または [Inertia](https://inertiajs.com) に基づくスキャフォールディング オプションを提供し、Inertiaベースのスキャフォールディングに Vue または React を使用することを選択できます。

<img src="https://laravel.com/img/docs/breeze-register.png">

#### Laravelブートキャンプ

Laravel を初めて使用する場合は、お気軽に [Laravelブートキャンプ](https://bootcamp.laravel.com) にアクセスしてください。 Laravel Bootcamp では、Breeze を使用して最初の Laravel アプリケーションを構築する手順を説明します。これは、Laravel と Breeze が提供するすべての機能を見学するのに最適な方法です。

<a name="laravel-breeze-installation"></a>
### インストール

まず、[新しいLaravelアプリケーションを作成する](/docs/{{version}}/installation) を実行し、データベースを構成し、[データベースの移行](/docs/{{version}}/migrations) を実行する必要があります。新しい Laravel アプリケーションを作成したら、Composer を使用して Laravel Breeze をインストールできます。

```shell
composer require laravel/breeze --dev
```

Composer が Laravel Breeze パッケージをインストールした後、`breeze:install` Artisan コマンドを実行できます。このコマンドは、認証ビュー、ルート、コントローラ、およびその他のリソースをアプリケーションに公開します。 Laravel Breeze はすべてのコードをアプリケーションに公開するため、その機能と実装を完全に制御し、可視化できます。

`breeze:install` コマンドを実行すると、優先するフロントエンド スタックとテスト フレームワークを指定するよう求められます。

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<a name="breeze-and-blade"></a>
### Breezeと刃

Breeze のデフォルトの「スタック」は Blade スタックで、単純な [Blade テンプレート](/docs/{{version}}/blade) を利用してアプリケーションのフロントエンドをレンダリングします。Blade スタックは、他の追加の引数を指定せずに `breeze:install` コマンドを呼び出し、Blade フロントエンド スタックを選択することでインストールできます。 Breeze のスキャフォールディングがインストールされたら、アプリケーションのフロントエンド アセットもコンパイルする必要があります。

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

次に、Web ブラウザでアプリケーションの `/login` または `/register` URL に移動します。 Breeze のルートはすべて、`routes/auth.php` ファイル内で定義されます。

> [!NOTE]  
> アプリケーションの CSS と JavaScript のコンパイルの詳細については、Laravel の [Vite ドキュメント](/docs/{{version}}/vite#running-vite) を確認してください。

<a name="breeze-and-livewire"></a>
### BreezeとLivewire

Laravel Breeze は [Livewire](https://livewire.laravel.com) 足場も提供しています。 Livewire は、PHP だけを使用して動的でリアクティブなフロントエンド UI を構築する強力な方法です。

Livewire は、主に Blade テンプレートを使用し、Vue や React などの JavaScript 駆動の SPA フレームワークのよりシンプルな代替手段を探しているチームに最適です。

Livewire スタックを使用するには、`breeze:install` Artisan コマンドを実行するときに Livewire フロントエンド スタックを選択できます。 Breeze のスキャフォールディングがインストールされたら、データベースの移行を実行する必要があります。

```shell
php artisan breeze:install

php artisan migrate
```

<a name="breeze-and-inertia"></a>
### Breeze と React / Vue

Laravel Breeze は、[Inertia](https://inertiajs.com) フロントエンド実装を介して React と Vue スキャフォールディングも提供します。 Inertia を使用すると、従来のサーバー側のルーティングとコントローラを使用して、最新の単一ページの React および Vue アプリケーションを構築できます。

Inertia を使用すると、React と Vue のフロントエンドのパワーを、Laravel の驚異的なバックエンドの生産性と超高速の [Vite](https://vitejs.dev) コンパイルと組み合わせて楽しむことができます。 Inertia スタックを使用するには、`breeze:install` Artisan コマンドの実行時に Vue または React フロントエンド スタックを選択できます。

Vue または React フロントエンド スタックを選択すると、Breeze インストーラーによって、[イナーシャSSR](https://inertiajs.com/server-side-rendering) または TypeScript のサポートを希望するかどうかを決定するよう求められます。 Breeze のスキャフォールディングがインストールされたら、アプリケーションのフロントエンド アセットもコンパイルする必要があります。

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

次に、Web ブラウザでアプリケーションの `/login` または `/register` URL に移動します。 Breeze のルートはすべて、`routes/auth.php` ファイル内で定義されます。

<a name="breeze-and-next"></a>
### Breeze と Next.js / API

Laravel Breeze は、[Next](https://nextjs.org)、[Nuxt](https://nuxt.com) などを利用した最新の JavaScript アプリケーションを認証する準備ができている認証 API をスキャフォールディングすることもできます。まず、`breeze:install` Artisan コマンドを実行するときに、目的のスタックとして API スタックを選択します。

```shell
php artisan breeze:install

php artisan migrate
```

インストール中に、Breeze は `FRONTEND_URL` 環境変数をアプリケーションの `.env` ファイルに追加します。この URL は、JavaScript アプリケーションの URL である必要があります。通常、ローカル開発中は `http://localhost:3000` になります。さらに、`APP_URL` が `http://localhost:8000` に設定されていることを確認する必要があります。これは、`serve` Artisan コマンドで使用されるデフォルトの URL です。

<a name="next-reference-implementation"></a>
#### Next.js リファレンス実装

最後に、このバックエンドを選択したフロントエンドと組み合わせる準備が整いました。 Breeze フロントエンドの次のリファレンス実装は、[GitHub で入手可能](https://github.com/laravel/breeze-next) です。このフロントエンドは Laravel によって保守されており、Breeze によって提供される従来の Blade および Inertia スタックと同じユーザー インターフェイスが含まれています。

<a name="laravel-jetstream"></a>
## Laravel Jetstream (Laravel Jetstream)

Laravel Breeze は Laravel アプリケーションを構築するためのシンプルかつ最小限の開始点を提供しますが、Jetstream はより堅牢な機能と追加のフロントエンド テクノロジ スタックでその機能を強化します。 **Laravel を初めて使用する方は、Laravel Jetstream を卒業する前に、Laravel Breeze でコツを学ぶことをお勧めします。**

Jetstream は、Laravel 用に美しく設計されたアプリケーション スキャフォールディングを提供します。これには、ログイン、登録、電子メール検証、2 要素認証、セッション管理、Laravel Sanctum を介した API サポート、およびオプションのチーム管理が含まれます。 Jetstream は [Tailwind CSS](https://tailwindcss.com) を使用して設計されており、[Livewire](https://livewire.laravel.com) または [Inertia](https://inertiajs.com) 駆動のフロントエンド スキャフォールディングを選択できます。

Laravel Jetstream のインストールに関する完全なドキュメントは、[Jetstreamの公式ドキュメント](https://jetstream.laravel.com) 内にあります。


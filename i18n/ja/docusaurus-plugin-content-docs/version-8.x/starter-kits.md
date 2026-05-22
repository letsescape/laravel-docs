# スターターキット (Starter Kits)

- [Introduction](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
    - [BreezeとInertia](#breeze-and-inertia)
    - [Breeze & Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## 導入 (Introduction)

新しい Laravel アプリケーションの構築をすぐに始められるように、認証およびアプリケーションのスターター キットを喜んで提供します。これらのキットは、アプリケーションのユーザーを登録および認証するために必要なルート、コントローラ、ビューを使用してアプリケーションを自動的にスキャフォールディングします。

これらのスターター キットを使用しても構いませんが、必須ではありません。 Laravel の新しいコピーをインストールするだけで、独自のアプリケーションを最初から自由に構築できます。いずれにせよ、私たちはあなたが素晴らしいものを作り上げることを確信しています。

<a name="laravel-breeze"></a>
## Laravel Breeze (Laravel Breeze)

[Laravel Breeze](https://github.com/laravel/breeze) は、ログイン、登録、パスワードのリセット、メール検証、パスワードの確認を含む、Laravel の [認証機能](/docs/{{version}}/authentication) のすべてを最小限にシンプルに実装したものです。 Laravel Breezeのデフォルトのビューレイヤーは、[Tailwind CSS](/docs/{{version}}/blade)でスタイル設定されたシンプルな[Blade テンプレート](https://tailwindcss.com)で構成されています。

Breeze は、新しい Laravel アプリケーションを開始するための素晴らしい出発点を提供し、[Laravel Livewire](https://laravel-livewire.com) を使用して Blade テンプレートを次のレベルに引き上げることを計画しているプロジェクトにも最適です。

<a name="laravel-breeze-installation"></a>
### インストール

まず、[新しいLaravelアプリケーションを作成する](/docs/{{version}}/installation) を実行し、データベースを構成し、[データベースの移行](/docs/{{version}}/migrations) を実行する必要があります。

```bash
curl -s https://laravel.build/example-app | bash

cd example-app

php artisan migrate
```

新しい Laravel アプリケーションを作成したら、Composer を使用して Laravel Breeze をインストールできます。

```bash
composer require laravel/breeze:1.9.2 
```

Composer が Laravel Breeze パッケージをインストールした後、`breeze:install` Artisan コマンドを実行できます。このコマンドは、認証ビュー、ルート、コントローラ、およびその他のリソースをアプリケーションに公開します。 Laravel Breeze はすべてのコードをアプリケーションに公開するため、その機能と実装を完全に制御し、可視化できます。 Breeze をインストールした後、アプリケーションの CSS ファイルを利用できるようにアセットをコンパイルする必要もあります。

```nothing
php artisan breeze:install

npm install
npm run dev
php artisan migrate
```

次に、Web ブラウザでアプリケーションの `/login` または `/register` URL に移動します。 Breeze のルートはすべて、`routes/auth.php` ファイル内で定義されます。

> {tip} アプリケーションの CSS と JavaScript のコンパイルの詳細については、[Laravel Mix ドキュメント](/docs/{{version}}/mix#running-mix) を確認してください。

<a name="breeze-and-inertia"></a>
### BreezeとInertia

Laravel Breeze は、Vue または React を利用した [Inertia.js](https://inertiajs.com) フロントエンド実装も提供します。 Inertia スタックを使用するには、`breeze:install` Artisan コマンドを実行するときに、希望するスタックとして `vue` または `react` を指定します。

```nothing
php artisan breeze:install vue

// Or...

php artisan breeze:install react

npm install
npm run dev
php artisan migrate
```

<a name="breeze-and-next"></a>
### Breeze & Next.js / API

Laravel Breeze は、[Next](https://nextjs.org)、[Nuxt](https://nuxt.com) などを利用した最新の JavaScript アプリケーションを認証する準備ができている認証 API をスキャフォールディングすることもできます。まず、`breeze:install` Artisan コマンドを実行するときに、目的のスタックとして `api` スタックを指定します。

```nothing
php artisan breeze:install api

php artisan migrate
```

インストール中に、Breeze は `FRONTEND_URL` 環境変数をアプリケーションの `.env` ファイルに追加します。この URL は、JavaScript アプリケーションの URL である必要があります。通常、ローカル開発中は `http://localhost:3000` になります。

<a name="next-reference-implementation"></a>
#### Next.js リファレンス実装

最後に、このバックエンドを選択したフロントエンドと組み合わせる準備が整いました。 Breeze フロントエンドの次のリファレンス実装は、[GitHub で入手可能](https://github.com/laravel/breeze-next) です。このフロントエンドは Laravel によって保守されており、Breeze によって提供される従来の Blade および Inertia スタックと同じユーザー インターフェイスが含まれています。

<a name="laravel-jetstream"></a>
## Laravel Jetstream (Laravel Jetstream)

Laravel Breeze は Laravel アプリケーションを構築するためのシンプルかつ最小限の開始点を提供しますが、Jetstream はより堅牢な機能と追加のフロントエンド テクノロジ スタックでその機能を強化します。 **Laravel を初めて使用する方は、Laravel Jetstream を卒業する前に、Laravel Breeze でコツを学ぶことをお勧めします。**

Jetstream は、Laravel 用に美しく設計されたアプリケーション スキャフォールディングを提供します。これには、ログイン、登録、電子メール検証、2 要素認証、セッション管理、Laravel Sanctum を介した API サポート、およびオプションのチーム管理が含まれます。 Jetstream は [Tailwind CSS](https://tailwindcss.com) を使用して設計されており、[Livewire](https://laravel-livewire.com) または [Inertia.js](https://inertiajs.com) 駆動のフロントエンド スキャフォールディングを選択できます。

Laravel Jetstream のインストールに関する完全なドキュメントは、[Jetstreamの公式ドキュメント](https://jetstream.laravel.com/introduction.html) 内にあります。


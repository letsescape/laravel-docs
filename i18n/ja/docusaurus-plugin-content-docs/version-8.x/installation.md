---
slug: /
---

# インストール (Installation)

- [Laravel について](#meet-laravel)
    - [なぜLaravelなのか?](#why-laravel)
- [初めての Laravel プロジェクト](#your-first-laravel-project)
    - [macOS での使用開始](#getting-started-on-macos)
    - [Windows での使用開始](#getting-started-on-windows)
    - [Linux の入門](#getting-started-on-linux)
    - [Sail サービスの選択](#choosing-your-sail-services)
    - [Composer によるインストール](#installation-via-composer)
- [初期設定](#initial-configuration)
    - [環境ベースの構成](#environment-based-configuration)
    - [ディレクトリ構成](#directory-configuration)
- [次のステップ](#next-steps)
    - [Laravel フルスタックフレームワーク](#laravel-the-fullstack-framework)
    - [Laravel API バックエンド](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel について (Meet Laravel)

Laravel は、表現力豊かでエレガントな構文を備えた Web アプリケーション フレームワークです。 Web フレームワークは、アプリケーション作成の構造と開始点を提供するため、私たちが詳細に取り組んでいる間、ユーザーは素晴らしいものを作成することに集中できます。

Laravel は、徹底した依存関係の注入、表現力豊かなデータベース抽象化レイヤー、キューとスケジュールされたジョブ、単体テストと統合テストなどの強力な機能を提供しながら、素晴らしい開発者エクスペリエンスを提供するよう努めています。

PHP や Web フレームワークを初めて使用する場合でも、長年の経験がある場合でも、Laravel はあなたとともに成長できるフレームワークです。私たちは、Web 開発者としての最初の一歩を踏み出すお手伝いをしたり、専門知識を次のレベルに引き上げるサポートを提供します。あなたが何を構築するのか楽しみです。

<a name="why-laravel"></a>
### なぜLaravelなのか?

Web アプリケーションを構築するときに利用できるさまざまなツールやフレームワークがあります。ただし、最新のフルスタック Web アプリケーションを構築するには Laravel が最適な選択であると考えています。

#### 進歩的なフレームワーク

私たちは Laravel を「進歩的な」フレームワークと呼びたいと思っています。つまり、Laravel はあなたとともに成長するということです。 Web 開発への最初の一歩を踏み出したばかりの場合、Laravel のドキュメント、ガイド、[ビデオチュートリアル](https://laracasts.com) の膨大なライブラリは、圧倒されることなくコツを学ぶのに役立ちます。

あなたが上級開発者であれば、Laravel は [依存性注入](/docs/{{version}}/container)、[単体テスト](/docs/{{version}}/testing)、[queues](/docs/{{version}}/queues)、[リアルタイムイベント](/docs/{{version}}/broadcasting) などのための強力なツールを提供します。 Laravel は、プロフェッショナルな Web アプリケーションを構築するために微調整されており、エンタープライズのワークロードを処理する準備ができています。

#### スケーラブルなフレームワーク

Laravel は信じられないほどスケーラブルです。 PHP のスケーリングに適した性質と、Redis などの高速分散キャッシュ システムに対する Laravel の組み込みサポートのおかげで、Laravel による水平スケーリングは簡単です。実際、Laravel アプリケーションは、月あたり数億のリクエストを処理できるように簡単に拡張できます。

極端なスケーリングが必要ですか? [Laravel Vapor](https://vapor.laravel.com) のようなプラットフォームを使用すると、AWS の最新のサーバーレステクノロジー上でほぼ無制限のスケールで Laravel アプリケーションを実行できます。

#### コミュニティの枠組み

Laravel は、PHP エコシステムの最高のパッケージを組み合わせて、利用可能な最も堅牢で開発者に優しいフレームワークを提供します。さらに、世界中の何千人もの才能ある開発者が [枠組みに貢献した](https://github.com/laravel/framework) を持っています。もしかしたら、あなたも Laravel のコントリビューターになれるかも知れません。

<a name="your-first-laravel-project"></a>
## 初めての Laravel プロジェクト (Your First Laravel Project)

私たちは、Laravel をできるだけ簡単に始められるようにしたいと考えています。自分のコンピュータで Laravel プロジェクトを開発および実行するには、さまざまなオプションがあります。これらのオプションを後で検討することもできますが、Laravel では、[Docker](/docs/{{version}}/sail) を使用して Laravel プロジェクトを実行するための組み込みソリューションである [Sail](https://www.docker.com) が提供されています。

Docker は、ローカル コンピューターにインストールされているソフトウェアや構成に干渉しない、小型軽量の「コンテナー」でアプリケーションやサービスを実行するためのツールです。これは、Web サーバーやデータベースなどの複雑な開発ツールをパーソナル コンピューター上で構成したりセットアップしたりすることを心配する必要がないことを意味します。開始するには、[Dockerデスクトップ](https://www.docker.com/products/docker-desktop) をインストールするだけです。

Laravel Sail は、Laravel のデフォルトの Docker 構成と対話するための軽量のコマンドライン インターフェイスです。 Sail は、事前の Docker 経験を必要とせずに、PHP、MySQL、および Redis を使用して Laravel アプリケーションを構築するための優れた出発点を提供します。

> {tip} すでに Docker のエキスパートですか?心配しないで！ Sail に関するすべては、Laravel に含まれる `docker-compose.yml` ファイルを使用してカスタマイズできます。

<a name="getting-started-on-macos"></a>
### macOS での使用開始

Mac で開発していて、[Dockerデスクトップ](https://www.docker.com/products/docker-desktop) がすでにインストールされている場合は、単純なターミナル コマンドを使用して新しい Laravel プロジェクトを作成できます。たとえば、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```nothing
curl -s "https://laravel.build/example-app" | bash
```

もちろん、この URL の「example-app」はお好みのものに変更できます。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```nothing
cd example-app

./vendor/bin/sail up
```

初めて Sail `up` コマンドを実行すると、Sail のアプリケーション コンテナーがマシン上に構築されます。これには数分かかる場合があります。 **心配しないでください。その後の Sail の開始試行ははるかに速くなります。**

アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> {tip} Laravel Sail についてさらに詳しく知りたい場合は、[完全なドキュメント](/docs/{{version}}/sail) を確認してください。

<a name="getting-started-on-windows"></a>
### Windows での使用開始

Windows マシンに新しい Laravel アプリケーションを作成する前に、必ず [Dockerデスクトップ](https://www.docker.com/products/docker-desktop) をインストールしてください。次に、Windows Subsystem for Linux 2 (WSL2) がインストールされ、有効になっていることを確認する必要があります。 WSL を使用すると、Linux バイナリ実行可能ファイルを Windows 10 上でネイティブに実行できます。WSL2 をインストールして有効にする方法に関する情報は、Microsoft の [開発者環境のドキュメント](https://docs.microsoft.com/en-us/windows/wsl/install-win10) にあります。

> {tip} WSL2 をインストールして有効にした後、Docker デスクトップが [WSL2 バックエンドを使用するように構成されています](https://docs.docker.com/docker-for-windows/wsl/) であることを確認する必要があります。

次に、最初の Laravel プロジェクトを作成する準備が整いました。 [Windowsターミナル](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) を起動し、WSL2 Linux オペレーティング システムの新しいターミナル セッションを開始します。次に、単純なターミナル コマンドを使用して、新しい Laravel プロジェクトを作成できます。たとえば、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```nothing
curl -s https://laravel.build/example-app | bash
```

もちろん、この URL の「example-app」はお好みのものに変更できます。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```nothing
cd example-app

./vendor/bin/sail up
```

初めて Sail `up` コマンドを実行すると、Sail のアプリケーション コンテナーがマシン上に構築されます。これには数分かかる場合があります。 **心配しないでください。その後の Sail の開始試行ははるかに速くなります。**

アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> {tip} Laravel Sail についてさらに詳しく知りたい場合は、[完全なドキュメント](/docs/{{version}}/sail) を確認してください。

#### WSL2 内での開発

もちろん、WSL2 インストール内で作成された Laravel アプリケーション ファイルを変更できる必要があります。これを実現するには、Microsoft の [Visual Studioコード](https://code.visualstudio.com) エディターと、同社の [リモート開発](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 用のファーストパーティ拡張機能を使用することをお勧めします。

これらのツールをインストールしたら、Windows ターミナルを使用してアプリケーションのルート ディレクトリから `code .` コマンドを実行して、Laravel プロジェクトを開くことができます。

<a name="getting-started-on-linux"></a>
### Linux の入門

Linux で開発していて、[Docker Compose](https://docs.docker.com/compose/install/) がすでにインストールされている場合は、単純なターミナル コマンドを使用して新しい Laravel プロジェクトを作成できます。たとえば、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```nothing
curl -s https://laravel.build/example-app | bash
```

もちろん、この URL の「example-app」はお好みのものに変更できます。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```nothing
cd example-app

./vendor/bin/sail up
```

初めて Sail `up` コマンドを実行すると、Sail のアプリケーション コンテナーがマシン上に構築されます。これには数分かかる場合があります。 **心配しないでください。その後の Sail の開始試行ははるかに速くなります。**

アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> {tip} Laravel Sail についてさらに詳しく知りたい場合は、[完全なドキュメント](/docs/{{version}}/sail) を確認してください。

<a name="choosing-your-sail-services"></a>
### Sail サービスの選択

Sail 経由で新しい Laravel アプリケーションを作成する場合、`with` クエリ文字列変数を使用して、新しいアプリケーションの `docker-compose.yml` ファイルでどのサービスを構成するかを選択できます。利用可能なサービスには、`mysql`、`pgsql`、`mariadb`、`redis`、`memcached`、`meilisearch`、`minio`、`selenium`、および `mailhog` が含まれます。

```nothing
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

設定するサービスを指定しない場合は、`mysql`、`redis`、`meilisearch`、`mailhog`、および `selenium` のデフォルト スタックが設定されます。

<a name="installation-via-composer"></a>
### Composer によるインストール

コンピューターにすでに PHP と Composer がインストールされている場合は、Composer を直接使用して新しい Laravel プロジェクトを作成できます。アプリケーションの作成後、Artisan CLI の `serve` コマンドを使用して、Laravel のローカル開発サーバーを起動できます。

    composer create-project laravel/laravel:^8.0 example-app

    cd example-app

    php artisan serve

<a name="the-laravel-installer"></a>
#### Laravel インストーラー

または、Laravel インストーラーをグローバル Composer 依存関係としてインストールすることもできます。

```nothing
composer global require laravel/installer

laravel new example-app

cd example-app

php artisan serve
```

`laravel` 実行可能ファイルがシステムで見つけられるように、Composer のシステム全体のベンダー bin ディレクトリを `$PATH` に配置してください。このディレクトリは、オペレーティング システムに応じて異なる場所に存在します。ただし、一般的な場所には次のようなものがあります。

<div class="content-list" markdown="1">

- macOS: `$HOME/.composer/vendor/bin`
- Windows: `%USERPROFILE%\AppData\Roaming\Composer\vendor\bin`
- GNU / Linux ディストリビューション: `$HOME/.config/composer/vendor/bin` または `$HOME/.composer/vendor/bin`

</div>

便宜上、Laravel インストーラーは新しいプロジェクト用の Git リポジトリを作成することもできます。 Git リポジトリを作成することを示すには、新しいプロジェクトの作成時に `--git` フラグを渡します。

```bash
laravel new example-app --git
```

このコマンドは、プロジェクトの新しい Git リポジトリを初期化し、基本 Laravel スケルトンを自動的にコミットします。 `git` フラグは、Git が適切にインストールおよび構成されていることを前提としています。 `--branch` フラグを使用して初期ブランチ名を設定することもできます。

```bash
laravel new example-app --git --branch="main"
```

`--git` フラグを使用する代わりに、`--github` フラグを使用して Git リポジトリを作成し、GitHub 上に対応するプライベート リポジトリを作成することもできます。

```bash
laravel new example-app --github
```

作成されたリポジトリは、`https://github.com/<your-account>/example-app` で利用できるようになります。 `github` フラグは、[GitHub CLI](https://cli.github.com) が適切にインストールされており、GitHub で認証されていることを前提としています。さらに、`git` がインストールされ、適切に構成されている必要があります。必要に応じて、GitHub CLI でサポートされている追加のフラグを渡すことができます。

```bash
laravel new example-app --github="--public"
```

`--organization` フラグを使用して、特定の GitHub 組織の下にリポジトリを作成できます。

```bash
laravel new example-app --github="--public" --organization="laravel"
```

<a name="initial-configuration"></a>
## 初期設定 (Initial Configuration)

Laravel フレームワークの構成ファイルはすべて、`config` ディレクトリに保存されます。各オプションは文書化されているので、ファイルに目を通して、利用可能なオプションをよく理解してください。

Laravel では、すぐに使用できる追加の構成はほとんど必要ありません。自由に開発を始めることができます。ただし、`config/app.php` ファイルとそのドキュメントを確認することをお勧めします。これには、`timezone` や `locale` などのいくつかのオプションが含まれており、アプリケーションに応じて変更できます。

<a name="environment-based-configuration"></a>
### 環境ベースの構成

Laravel の構成オプション値の多くは、アプリケーションがローカル コンピューターで実行されているか実稼働 Web サーバーで実行されているかによって異なる場合があるため、多くの重要な構成値は、アプリケーションのルートに存在する `.env` ファイルを使用して定義されます。

アプリケーションを使用する各開発者/サーバーは異なる環境構成を必要とする可能性があるため、`.env` ファイルをアプリケーションのソース管理にコミットしないでください。さらに、侵入者がソース管理リポジトリにアクセスした場合、機密の資格情報が漏洩してしまうため、セキュリティ リスクとなります。

> {tip} `.env` ファイルと環境ベースの構成の詳細については、完全な [設定ドキュメント](/docs/{{version}}/configuration#environment-configuration) を確認してください。

<a name="directory-configuration"></a>
### ディレクトリ構成

Laravel は常に、Web サーバーに設定された「Web ディレクトリ」のルートから提供される必要があります。 「Web ディレクトリ」のサブディレクトリから Laravel アプリケーションを提供しようとしないでください。これを試みると、アプリケーション内に存在する機密ファイルが公開される可能性があります。

<a name="next-steps"></a>
## 次のステップ (Next Steps)

Laravel プロジェクトを作成したので、次に何を学べばよいのか疑問に思っているかもしれません。まず、次のドキュメントを読んで、Laravel がどのように動作するかを理解することを強くお勧めします。

<div class="content-list" markdown="1">

- [リクエストのライフサイクル](/docs/{{version}}/lifecycle)
- [Configuration](/docs/{{version}}/configuration)
- [ディレクトリ構造](/docs/{{version}}/structure)
- [サービスコンテナ](/docs/{{version}}/container)
- [Facades](/docs/{{version}}/facades)

</div>

Laravel をどのように使用したいかによって、旅の次のステップも決まります。 Laravel を使用するにはさまざまな方法がありますが、以下ではフレームワークの 2 つの主な使用例を検討します。

<a name="laravel-the-fullstack-framework"></a>
### Laravel フルスタックフレームワーク

Laravel はフルスタック フレームワークとして機能する可能性があります。 「フルスタック」フレームワークとは、Laravel を使用してリクエストをアプリケーションにルーティングし、[Blade テンプレート](/docs/{{version}}/blade) 経由で、または [Inertia.js](https://inertiajs.com) のような単一ページ アプリケーションのハイブリッド テクノロジを使用してフロントエンドをレンダリングすることを意味します。これは、Laravel フレームワークを使用する最も一般的な方法です。

これが Laravel の使用方法である場合は、[routing](/docs/{{version}}/routing)、[views](/docs/{{version}}/views)、または [Eloquent ORM](/docs/{{version}}/eloquent) に関するドキュメントを確認してください。さらに、[Livewire](https://laravel-livewire.com) や [Inertia.js](https://inertiajs.com) などのコミュニティ パッケージについても興味があるかもしれません。これらのパッケージを使用すると、シングルページ JavaScript アプリケーションによって提供される UI の利点の多くを享受しながら、Laravel をフルスタック フレームワークとして使用できるようになります。

Laravel をフルスタック フレームワークとして使用している場合は、[Laravel Mix](/docs/{{version}}/mix) を使用してアプリケーションの CSS と JavaScript をコンパイルする方法を学習することも強くお勧めします。

> {tip} アプリケーションの構築をいち早く始めたい場合は、公式 [アプリケーションスターターキット](/docs/{{version}}/starter-kits) をチェックしてください。

<a name="laravel-the-api-backend"></a>
### Laravel API バックエンド

Laravel は、JavaScript シングルページ アプリケーションまたはモバイル アプリケーションへの API バックエンドとしても機能します。たとえば、[Next.js](https://nextjs.org) アプリケーションの API バックエンドとして Laravel を使用することができます。このコンテキストでは、Laravel を使用してアプリケーションに [authentication](/docs/{{version}}/sanctum) とデータ ストレージ/取得を提供すると同時に、キュー、電子メール、通知などの Laravel の強力なサービスも利用できます。

これが Laravel の使用方法である場合は、[routing](/docs/{{version}}/routing)、[Laravel Sanctum](/docs/{{version}}/sanctum)、および [Eloquent ORM](/docs/{{version}}/eloquent) に関するドキュメントを確認してください。

> {tip} Laravel バックエンドと Next.js フロントエンドのスキャフォールディングを早めに始める必要がありますか? Laravel Breeze は [Next.js フロントエンドの実装](/docs/{{version}}/starter-kits#breeze-and-next) だけでなく [APIスタック](https://github.com/laravel/breeze-next) も提供しているので、数分で開始できます。



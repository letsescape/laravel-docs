---
slug: /
---

# インストール (Installation)

- [Laravel について](#meet-laravel)
    - [なぜLaravelなのか?](#why-laravel)
- [Laravelプロジェクトの作成](#creating-a-laravel-project)
- [初期設定](#initial-configuration)
    - [環境ベースの構成](#environment-based-configuration)
    - [データベースと移行](#databases-and-migrations)
    - [ディレクトリ構成](#directory-configuration)
- [Sail を使用した Docker のインストール](#docker-installation-using-sail)
    - [macOS で航海する](#sail-on-macos)
    - [Windows で航海する](#sail-on-windows)
    - [Linux で航海する](#sail-on-linux)
    - [Sail サービスの選択](#choosing-your-sail-services)
- [IDEのサポート](#ide-support)
- [LaravelとAI](#laravel-and-ai)
    - [Laravel Boostのインストール](#installing-laravel-boost)
- [次のステップ](#next-steps)
    - [Laravel フルスタックフレームワーク](#laravel-the-fullstack-framework)
    - [Laravel API バックエンド](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel について (Meet Laravel)

Laravel は、表現力豊かでエレガントな構文を備えた Web アプリケーション フレームワークです。 Web フレームワークは、アプリケーション作成の構造と開始点を提供するため、私たちが詳細に取り組んでいる間、ユーザーは素晴らしいものを作成することに集中できます。

Laravel は、徹底した依存関係の注入、表現力豊かなデータベース抽象化レイヤー、キューとスケジュールされたジョブ、単体テストと統合テストなどの強力な機能を提供しながら、素晴らしい開発者エクスペリエンスを提供するよう努めています。

PHP Web フレームワークを初めて使用する場合でも、長年の経験がある場合でも、Laravel はあなたとともに成長できるフレームワークです。私たちは、Web 開発者としての最初の一歩を踏み出すお手伝いをしたり、専門知識を次のレベルに引き上げるサポートを提供します。あなたが何を構築するのか楽しみです。

> [!NOTE]  
> Laravel は初めてですか?最初の Laravel アプリケーションを構築する手順を説明しながら、フレームワークの実践的なツアーについては、[Laravelブートキャンプ](https://bootcamp.laravel.com) をご覧ください。

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

<a name="creating-a-laravel-project"></a>
## Laravelプロジェクトの作成 (Creating a Laravel Project)

最初の Laravel プロジェクトを作成する前に、ローカル マシンに PHP と [Composer](https://getcomposer.org) がインストールされていることを確認してください。 macOS で開発している場合は、[LaravelのHerd](https://herd.laravel.com) を介して PHP と Composer を数分でインストールできます。また、[ノードとNPMのインストール](https://nodejs.org) を推奨します。

PHP と Composer をインストールした後、Composer の `create-project` コマンドを使用して新しい Laravel プロジェクトを作成できます。

```nothing
composer create-project "laravel/laravel:^10.0" example-app
```

または、Composer 経由で [Laravelインストーラー](https://github.com/laravel/installer) をグローバルにインストールすることで、新しい Laravel プロジェクトを作成することもできます。

```nothing
composer global require laravel/installer

laravel new example-app
```

プロジェクトが作成されたら、Laravel Artisan の `serve` コマンドを使用して、Laravel のローカル開発サーバーを起動します。

```nothing
cd example-app

php artisan serve
```

Artisan 開発サーバーを起動すると、Web ブラウザ ([http://localhost:8000](http://localhost:8000)) でアプリケーションにアクセスできるようになります。次に、[Laravelエコシステムへの次の一歩を踏み出しましょう](#next-steps) の準備が整いました。もちろん、[データベースを構成する](#databases-and-migrations) することもできます。

> [!NOTE]  
> Laravel アプリケーションの開発を早く始めたい場合は、[スターターキット](/docs/{{version}}/starter-kits) のいずれかの使用を検討してください。 Laravel のスターター キットは、新しい Laravel アプリケーションにバックエンドおよびフロントエンドの認証スキャフォールディングを提供します。

<a name="initial-configuration"></a>
## 初期設定 (Initial Configuration)

Laravel フレームワークの構成ファイルはすべて、`config` ディレクトリに保存されます。各オプションは文書化されているので、ファイルに目を通して、利用可能なオプションをよく理解してください。

Laravel では、すぐに使用できる追加の構成はほとんど必要ありません。自由に開発を始めることができます。ただし、`config/app.php` ファイルとそのドキュメントを確認することをお勧めします。これには、`timezone` や `locale` などのいくつかのオプションが含まれており、アプリケーションに応じて変更できます。

<a name="environment-based-configuration"></a>
### 環境ベースの構成

Laravel の構成オプション値の多くは、アプリケーションがローカル マシンで実行されているか実稼働 Web サーバーで実行されているかによって異なる場合があるため、多くの重要な構成値は、アプリケーションのルートに存在する `.env` ファイルを使用して定義されます。

アプリケーションを使用する各開発者/サーバーは異なる環境構成を必要とする可能性があるため、`.env` ファイルをアプリケーションのソース管理にコミットしないでください。さらに、侵入者がソース管理リポジトリにアクセスした場合、機密の資格情報が漏洩してしまうため、セキュリティ リスクとなります。

> [!NOTE]  
> `.env` ファイルと環境ベースの構成の詳細については、完全な [設定ドキュメント](/docs/{{version}}/configuration#environment-configuration) を確認してください。

<a name="databases-and-migrations"></a>
### データベースと移行

Laravel アプリケーションを作成したので、おそらくいくつかのデータをデータベースに保存したいと思うでしょう。デフォルトでは、アプリケーションの `.env` 構成ファイルは、Laravel が MySQL データベースと対話し、`127.0.0.1` でデータベースにアクセスすることを指定します。

> [!NOTE]  
> macOS で開発していて、MySQL、Postgres、または Redis をローカルにインストールする必要がある場合は、[DBngin](https://dbngin.com/) の使用を検討してください。

MySQL または Postgres をローカル マシンにインストールしたくない場合は、いつでも [SQLite](https://www.sqlite.org/index.html) データベースを使用できます。 SQLite は、小型、高速、自己完結型のデータベース エンジンです。まず、Laravel の `sqlite` データベースドライバを使用するように `.env` 構成ファイルを更新します。他のデータベース構成オプションは削除できます。

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

SQLite データベースを構成したら、アプリケーションの [データベースの移行](/docs/{{version}}/migrations) を実行すると、アプリケーションのデータベース テーブルが作成されます。

```shell
php artisan migrate
```

アプリケーションに SQLite データベースが存在しない場合、Laravel はデータベースを作成するかどうかを尋ねます。通常、SQLite データベース ファイルは `database/database.sqlite` に作成されます。

<a name="directory-configuration"></a>
### ディレクトリ構成

Laravel は常に、Web サーバーに設定された「Web ディレクトリ」のルートから提供される必要があります。 「Web ディレクトリ」のサブディレクトリから Laravel アプリケーションを提供しようとしないでください。これを試みると、アプリケーション内に存在する機密ファイルが公開される可能性があります。

<a name="docker-installation-using-sail"></a>
## Sail を使用した Docker のインストール (Docker Installation Using Sail)

私たちは、好みのオペレーティング システムに関係なく、できるだけ簡単に Laravel を始められるようにしたいと考えています。したがって、ローカルマシン上で Laravel プロジェクトを開発および実行するには、さまざまなオプションがあります。これらのオプションを後で検討することもできますが、Laravel では、[Docker](/docs/{{version}}/sail) を使用して Laravel プロジェクトを実行するための組み込みソリューションである [Sail](https://www.docker.com) が提供されています。

Docker は、ローカル マシンにインストールされているソフトウェアや構成に干渉しない、小型軽量の「コンテナ」でアプリケーションやサービスを実行するためのツールです。これは、ローカル マシン上で Web サーバーやデータベースなどの複雑な開発ツールの構成やセットアップについて心配する必要がないことを意味します。開始するには、[Dockerデスクトップ](https://www.docker.com/products/docker-desktop) をインストールするだけです。

Laravel Sail は、Laravel のデフォルトの Docker 構成と対話するための軽量のコマンドライン インターフェイスです。 Sail は、事前の Docker 経験を必要とせずに、PHP、MySQL、および Redis を使用して Laravel アプリケーションを構築するための優れた出発点を提供します。

> [!NOTE]  
> すでに Docker の専門家ですか?心配しないで！ Sail に関するすべては、Laravel に含まれる `docker-compose.yml` ファイルを使用してカスタマイズできます。

<a name="sail-on-macos"></a>
### macOS で航海する

Mac で開発していて、[Dockerデスクトップ](https://www.docker.com/products/docker-desktop) がすでにインストールされている場合は、単純なターミナル コマンドを使用して新しい Laravel プロジェクトを作成できます。たとえば、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```shell
curl -s "https://laravel.build/example-app" | bash
```

もちろん、この URL の「example-app」を好きなものに変更できます。ただし、アプリケーション名には英数字、ダッシュ、アンダースコアのみが含まれていることを確認してください。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

Sail のアプリケーション コンテナーがローカル マシン上に構築されるまで、Sail のインストールには数分かかる場合があります。

プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```shell
cd example-app

./vendor/bin/sail up
```

アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> [!NOTE]  
> Laravel Sail についてさらに学習するには、[完全なドキュメント](/docs/{{version}}/sail) を参照してください。

<a name="sail-on-windows"></a>
### Windows で航海する

Windows マシンに新しい Laravel アプリケーションを作成する前に、必ず [Dockerデスクトップ](https://www.docker.com/products/docker-desktop) をインストールしてください。次に、Windows Subsystem for Linux 2 (WSL2) がインストールされ、有効になっていることを確認する必要があります。 WSL を使用すると、Linux バイナリ実行可能ファイルを Windows 10 上でネイティブに実行できます。WSL2 をインストールして有効にする方法に関する情報は、Microsoft の [開発者環境のドキュメント](https://docs.microsoft.com/en-us/windows/wsl/install-win10) にあります。

> [!NOTE]  
> WSL2 をインストールして有効にした後、Docker Desktop が [WSL2 バックエンドを使用するように構成されています](https://docs.docker.com/docker-for-windows/wsl/) であることを確認する必要があります。

次に、最初の Laravel プロジェクトを作成する準備が整いました。 [Windowsターミナル](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) を起動し、WSL2 Linux オペレーティング システムの新しいターミナル セッションを開始します。次に、単純なターミナル コマンドを使用して、新しい Laravel プロジェクトを作成できます。たとえば、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```shell
curl -s https://laravel.build/example-app | bash
```

もちろん、この URL の「example-app」を好きなものに変更できます。ただし、アプリケーション名には英数字、ダッシュ、アンダースコアのみが含まれていることを確認してください。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

Sail のアプリケーション コンテナーがローカル マシン上に構築されるまで、Sail のインストールには数分かかる場合があります。

プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```shell
cd example-app

./vendor/bin/sail up
```

アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> [!NOTE]  
> Laravel Sail についてさらに学習するには、[完全なドキュメント](/docs/{{version}}/sail) を参照してください。

#### WSL2 内での開発

もちろん、WSL2 インストール内で作成された Laravel アプリケーション ファイルを変更できる必要があります。これを実現するには、Microsoft の [Visual Studioコード](https://code.visualstudio.com) エディターと、同社の [リモート開発](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 用のファーストパーティ拡張機能を使用することをお勧めします。

これらのツールをインストールしたら、Windows ターミナルを使用してアプリケーションのルート ディレクトリから `code .` コマンドを実行して、Laravel プロジェクトを開くことができます。

<a name="sail-on-linux"></a>
### Linux で航海する

Linux で開発していて、[Docker Compose](https://docs.docker.com/compose/install/) がすでにインストールされている場合は、単純なターミナル コマンドを使用して新しい Laravel プロジェクトを作成できます。

まず、Docker Desktop for Linux を使用している場合は、次のコマンドを実行する必要があります。 Linux 用 Docker Desktop を使用していない場合は、この手順をスキップできます。

```shell
docker context use default
```

次に、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```shell
curl -s https://laravel.build/example-app | bash
```

もちろん、この URL の「example-app」を好きなものに変更できます。ただし、アプリケーション名には英数字、ダッシュ、アンダースコアのみが含まれていることを確認してください。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

Sail のアプリケーション コンテナーがローカル マシン上に構築されるまで、Sail のインストールには数分かかる場合があります。

プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```shell
cd example-app

./vendor/bin/sail up
```

アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> [!NOTE]  
> Laravel Sail についてさらに学習するには、[完全なドキュメント](/docs/{{version}}/sail) を参照してください。

<a name="choosing-your-sail-services"></a>
### Sail サービスの選択

Sail 経由で新しい Laravel アプリケーションを作成する場合、`with` クエリ文字列変数を使用して、新しいアプリケーションの `docker-compose.yml` ファイルでどのサービスを構成するかを選択できます。利用可能なサービスには、`mysql`、`pgsql`、`mariadb`、`redis`、`memcached`、`meilisearch`、`typesense`、`minio`、`selenium`、および `mailpit` が含まれます。

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

設定するサービスを指定しない場合は、`mysql`、`redis`、`meilisearch`、`mailpit`、および `selenium` のデフォルト スタックが設定されます。

URL に `devcontainer` パラメータを追加することで、デフォルトの [Devcontainer](/docs/{{version}}/sail#using-devcontainers) をインストールするように Sail に指示できます。

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
## IDEのサポート (IDE Support)

Laravel アプリケーションを開発する際には、任意のコード エディタを自由に使用できます。ただし、[PhpStorm](https://www.jetbrains.com/phpstorm/laravel/) は、[LaravelPint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html) を含む、Laravel とそのエコシステムに対する広範なサポートを提供します。

さらに、コミュニティが管理する [Laravelのアイデア](https://laravel-idea.com/) PhpStorm プラグインは、コード生成、Eloquent 構文補完、検証ルール補完など、さまざまな便利な IDE 拡張機能を提供します。

<a name="laravel-and-ai"></a>
## LaravelとAI (Laravel and AI)

[Laravelブースト](https://github.com/laravel/boost) は、AI コーディング エージェントと Laravel アプリケーションの間のギャップを埋める強力なツールです。 Boost は、AI エージェントに Laravel 固有のコンテキスト、ツール、ガイドラインを提供するため、Laravel の規則に従って、より正確なバージョン固有のコードを生成できます。

Laravel アプリケーションに Boost をインストールすると、AI エージェントは、使用しているパッケージの把握、データベースのクエリ、Laravel ドキュメントの検索、ブラウザのログの読み取り、テストの生成、Tinker 経由のコードの実行など、15 を超える特殊なツールにアクセスできるようになります。

さらに、Boost を使用すると、AI エージェントは、インストールされているパッケージのバージョンに応じて、17,000 を超えるベクトル化された Laravel エコシステム ドキュメントにアクセスできるようになります。これは、エージェントがプロジェクトで使用する正確なバージョンを対象としたガイダンスを提供できることを意味します。

Boost には、エージェントがフレームワークの規則に従い、適切なテストを作成し、Laravel コード生成時によくある落とし穴を回避するように促す、Laravel が管理する AI ガイドラインも含まれています。

<a name="installing-laravel-boost"></a>
### Laravel Boostのインストール

Boost は、PHP 8.1 以降を実行している Laravel 10、11、12 アプリケーションにインストールできます。まず、Boost を開発依存関係としてインストールします。

```shell
composer require laravel/boost --dev
```

インストールしたら、対話型インストーラーを実行します。

```shell
php artisan boost:install
```

インストーラーは IDE および AI エージェントを自動検出し、プロジェクトに適した機能を選択できるようにします。 Boost は既存のプロジェクトの規則を尊重し、デフォルトでは独自のスタイル ルールを強制しません。

> [!NOTE]
> ブーストの詳細については、[GitHub 上の Laravel Boost リポジトリ](https://github.com/laravel/boost) をご覧ください。

<a name="next-steps"></a>
## 次のステップ (Next Steps)

Laravel プロジェクトを作成したので、次に何を学べばよいのか疑問に思っているかもしれません。まず、次のドキュメントを読んで、Laravel がどのように動作するかを理解することを強くお勧めします。

<div class="content-list" markdown="1">

- [リクエストのライフサイクル](/docs/{{version}}/lifecycle)
- [Configuration](/docs/{{version}}/configuration)
- [ディレクトリ構造](/docs/{{version}}/structure)
- [Frontend](/docs/{{version}}/frontend)
- [サービスコンテナ](/docs/{{version}}/container)
- [Facades](/docs/{{version}}/facades)

</div>

Laravel をどのように使用したいかによって、旅の次のステップも決まります。 Laravel を使用するにはさまざまな方法がありますが、以下ではフレームワークの 2 つの主な使用例を検討します。

> [!NOTE]  
> Laravel は初めてですか?最初の Laravel アプリケーションを構築する手順を説明しながら、フレームワークの実践的なツアーについては、[Laravelブートキャンプ](https://bootcamp.laravel.com) をご覧ください。

<a name="laravel-the-fullstack-framework"></a>
### Laravel フルスタックフレームワーク

Laravel はフルスタック フレームワークとして機能する可能性があります。 「フルスタック」フレームワークとは、Laravel を使用してリクエストをアプリケーションにルーティングし、[Blade テンプレート](/docs/{{version}}/blade) または [Inertia](https://inertiajs.com) のような単一ページ アプリケーションのハイブリッド テクノロジを介してフロントエンドをレンダリングすることを意味します。これは、Laravel フレームワークを使用する最も一般的な方法であり、私たちの意見では、Laravel を使用する最も生産的な方法です。

これが Laravel の使用方法である場合は、[フロントエンド開発](/docs/{{version}}/frontend)、[routing](/docs/{{version}}/routing)、[views](/docs/{{version}}/views)、または [Eloquent ORM](/docs/{{version}}/eloquent) に関するドキュメントを確認してください。さらに、[Livewire](https://livewire.laravel.com) や [Inertia](https://inertiajs.com) などのコミュニティ パッケージについても興味があるかもしれません。これらのパッケージを使用すると、シングルページ JavaScript アプリケーションによって提供される UI の利点の多くを享受しながら、Laravel をフルスタック フレームワークとして使用できるようになります。

Laravel をフルスタック フレームワークとして使用している場合は、[Vite](/docs/{{version}}/vite) を使用してアプリケーションの CSS と JavaScript をコンパイルする方法を学習することも強くお勧めします。

> [!NOTE]  
> アプリケーションの構築をいち早く始めたい場合は、公式の [アプリケーションスターターキット](/docs/{{version}}/starter-kits) をチェックしてください。

<a name="laravel-the-api-backend"></a>
### Laravel API バックエンド

Laravel は、JavaScript シングルページ アプリケーションまたはモバイル アプリケーションへの API バックエンドとしても機能します。たとえば、[Next.js](https://nextjs.org) アプリケーションの API バックエンドとして Laravel を使用することができます。このコンテキストでは、Laravel を使用してアプリケーションに [authentication](/docs/{{version}}/sanctum) とデータ ストレージ/取得を提供すると同時に、キュー、電子メール、通知などの Laravel の強力なサービスも利用できます。

これが Laravel の使用方法である場合は、[routing](/docs/{{version}}/routing)、[Laravel Sanctum](/docs/{{version}}/sanctum)、および [Eloquent ORM](/docs/{{version}}/eloquent) に関するドキュメントを確認してください。

> [!NOTE]  
> Laravel バックエンドと Next.js フロントエンドのスキャフォールディングをいち早く始める必要がありますか? Laravel Breeze は [Next.js フロントエンドの実装](/docs/{{version}}/starter-kits#breeze-and-next) だけでなく [APIスタック](https://github.com/laravel/breeze-next) も提供しているので、数分で開始できます。


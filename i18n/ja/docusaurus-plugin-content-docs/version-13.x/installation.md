---
slug: /
---

# インストール (Installation)

- [Laravel について](#meet-laravel)
    - [なぜLaravelなのか?](#why-laravel)
- [Laravelアプリケーションの作成](#creating-a-laravel-project)
    - [AI の使用を開始する](#getting-started-using-ai)
    - [PHP と Laravel インストーラーのインストール](#installing-php)
    - [アプリケーションの作成](#creating-an-application)
- [初期設定](#initial-configuration)
    - [環境ベースの構成](#environment-based-configuration)
    - [データベースと移行](#databases-and-migrations)
    - [ディレクトリ構成](#directory-configuration)
- [Herd を使用したインストール](#installation-using-herd)
    - [macOS 上のHerd](#herd-on-macos)
    - [Windows 上のHerd](#herd-on-windows)
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

<a name="why-laravel"></a>
### なぜLaravelなのか?

Web アプリケーションを構築するときに利用できるさまざまなツールやフレームワークがあります。ただし、最新のフルスタック Web アプリケーションを構築するには Laravel が最適な選択であると考えています。

#### 進歩的なフレームワーク

私たちは Laravel を「進歩的な」フレームワークと呼びたいと思っています。つまり、Laravel はあなたとともに成長するということです。 Web 開発への最初の一歩を踏み出したばかりの場合、Laravel のドキュメント、ガイド、[ビデオチュートリアル](https://laracasts.com) の膨大なライブラリは、圧倒されることなくコツを学ぶのに役立ちます。

あなたが上級開発者であれば、Laravel は [依存性注入](/docs/{{version}}/container)、[単体テスト](/docs/{{version}}/testing)、[queues](/docs/{{version}}/queues)、[リアルタイムイベント](/docs/{{version}}/broadcasting) などのための強力なツールを提供します。 Laravel はプロフェッショナルな Web アプリケーションを構築するために微調整されており、エンタープライズ ワークロードを処理する準備ができています。

#### スケーラブルなフレームワーク

Laravel は信じられないほどスケーラブルです。 PHP のスケーリングに適した性質と、Redis などの高速分散キャッシュ システムに対する Laravel の組み込みサポートのおかげで、Laravel による水平スケーリングは簡単です。実際、Laravel アプリケーションは、月あたり数億のリクエストを処理できるように簡単に拡張できます。

極端なスケーリングが必要ですか? [Laravel Cloud](https://cloud.laravel.com) のようなプラットフォームを使用すると、Laravel アプリケーションをほぼ無制限のスケールで実行できます。

#### エージェント対応フレームワーク

Laravel の独自の規約と明確に定義された構造により、Cursor や Claude Code などのツールを使用する [AI支援開発](/docs/{{version}}/ai) にとって理想的なフレームワークになります。 AI エージェントにコントローラの追加を依頼すると、AI エージェントはコントローラを配置する場所を正確に認識します。新しい移行が必要な場合、命名規則とファイルの場所は予測可能です。この一貫性により、より柔軟なフレームワークで AI ツールをつまずかせる推測作業が排除されます。

ファイル構成を超えて、Laravel の表現力豊かな構文と包括的なドキュメントは、AI エージェントに正確で慣用的なコードを生成するために必要なコンテキストを提供します。 Eloquent リレーションシップ、フォーム リクエスト、ミドルウェアなどの機能は、エージェントが確実に理解して複製できるパターンに従います。その結果、AI によって生成されたコードは、一般的な PHP スニペットをつなぎ合わせたものではなく、熟練した Laravel 開発者によって書かれたように見えます。

Laravel が AI 支援開発に最適な選択肢である理由について詳しくは、[エージェントの開発](/docs/{{version}}/ai) のドキュメントをご覧ください。

#### コミュニティの枠組み

Laravel は、PHP エコシステムの最高のパッケージを組み合わせて、利用可能な最も堅牢で開発者に優しいフレームワークを提供します。さらに、世界中の何千人もの才能ある開発者が [枠組みに貢献した](https://github.com/laravel/framework) を持っています。もしかしたら、あなたも Laravel のコントリビューターになれるかも知れません。

<a name="creating-a-laravel-project"></a>
## Laravelアプリケーションの作成 (Creating a Laravel Application)

<a name="getting-started-using-ai"></a>
### AI の使用を開始する

[クロード・コード](https://docs.anthropic.com/en/docs/claude-code) や [OpenCode](https://opencode.ai) などの AI コーディング エージェントを使用している場合は、プロジェクトに触れる前にエージェントに Laravel 固有の Playbook を提供するプロンプトから始めることができます。

以下のプロンプトは、エージェントに、Laravel のインストール ガイダンスの場所、何を優先するか、まだ選択していない場合に適切なデフォルトを設定する方法を示します。これをエージェントに貼り付けて開始します。

```text
I'm building a new Laravel application.

Fetch and follow the instructions from https://laravel.com/for/agents. Treat the returned Markdown as the source of truth for how to install and set up Laravel in this session.
```

エージェントが手順を読んだ後、段階的にガイドし、セットアップを Laravel のデフォルトに合わせて維持します。

<a name="installing-php"></a>
### PHP と Laravel インストーラーのインストール

最初の Laravel アプリケーションを作成する前に、ローカル マシンに [PHP](https://php.net)、[Composer](https://getcomposer.org)、および [Laravelインストーラー](https://github.com/laravel/installer) がインストールされていることを確認してください。さらに、アプリケーションのフロントエンド アセットをコンパイルできるように、[ノードとNPM](https://nodejs.org) または [Bun](https://bun.sh/) をインストールする必要があります。

ローカル マシンに PHP と Composer がインストールされていない場合は、次のコマンドで PHP、Composer、および Laravel インストーラーを macOS、Windows、または Linux にインストールします。

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.5)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.5'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.5)"
```

上記のコマンドのいずれかを実行した後、ターミナル セッションを再起動する必要があります。 `php.new` 経由でインストールした後に PHP、Composer、および Laravel インストーラーを更新するには、ターミナルでコマンドを再実行します。

すでに PHP と Composer がインストールされている場合は、Composer 経由で Laravel インストーラーをインストールできます。

```shell
composer global require laravel/installer
```

> [!NOTE]
> フル機能のグラフィカルな PHP のインストールと管理エクスペリエンスについては、[LaravelのHerd](#installation-using-herd) をチェックしてください。

<a name="creating-an-application"></a>
### アプリケーションの作成

PHP、Composer、および Laravel インストーラーをインストールしたら、新しい Laravel アプリケーションを作成する準備が整います。 Laravel インストーラーは、好みのテスト フレームワーク、データベース、スターター キットを選択するよう求めます。

```shell
laravel new example-app
```

アプリケーションが作成されたら、`dev` Composer スクリプトを使用して、Laravel のローカル開発サーバー、キューワーカー、および Vite 開発サーバーを起動できます。

```shell
cd example-app
npm install && npm run build
composer run dev
```

開発サーバーを起動すると、Web ブラウザ ([http://localhost:8000](http://localhost:8000)) でアプリケーションにアクセスできるようになります。次に、[Laravelエコシステムへの次の一歩を踏み出しましょう](#next-steps) の準備が整いました。もちろん、[データベースを構成する](#databases-and-migrations) することもできます。

> [!NOTE]
> Laravel アプリケーションの開発を早く始めたい場合は、[スターターキット](/docs/{{version}}/starter-kits) のいずれかの使用を検討してください。 Laravel のスターター キットは、新しい Laravel アプリケーションにバックエンドおよびフロントエンドの認証スキャフォールディングを提供します。

<a name="initial-configuration"></a>
## 初期設定 (Initial Configuration)

Laravel フレームワークの構成ファイルはすべて、`config` ディレクトリに保存されます。各オプションは文書化されているので、ファイルに目を通して、利用可能なオプションをよく理解してください。

Laravel では、すぐに使用できる追加の構成はほとんど必要ありません。自由に開発を始めることができます。ただし、`config/app.php` ファイルとそのドキュメントを確認することをお勧めします。これには、`url` や `locale` などのいくつかのオプションが含まれており、アプリケーションに応じて変更できます。

<a name="environment-based-configuration"></a>
### 環境ベースの構成

Laravel の構成オプション値の多くは、アプリケーションがローカル マシンで実行されているか実稼働 Web サーバーで実行されているかによって異なる場合があるため、多くの重要な構成値は、アプリケーションのルートに存在する `.env` ファイルを使用して定義されます。

アプリケーションを使用する各開発者/サーバーは異なる環境構成を必要とする可能性があるため、`.env` ファイルをアプリケーションのソース管理にコミットしないでください。さらに、侵入者がソース管理リポジトリにアクセスした場合、機密の資格情報が公開されるため、セキュリティ リスクになります。

> [!NOTE]
> `.env` ファイルと環境ベースの構成の詳細については、完全な [設定ドキュメント](/docs/{{version}}/configuration#environment-configuration) を確認してください。

<a name="databases-and-migrations"></a>
### データベースと移行

Laravel アプリケーションを作成したので、おそらくいくつかのデータをデータベースに保存したいと思うでしょう。デフォルトでは、アプリケーションの `.env` 構成ファイルは、Laravel が SQLite データベースと対話することを指定します。

アプリケーションの作成中に、Laravel は `database/database.sqlite` ファイルを作成し、アプリケーションのデータベーステーブルを作成するために必要な移行を実行しました。

MySQL や PostgreSQL などの別のデータベース ドライバを使用したい場合は、適切なデータベースを使用するように `.env` 構成ファイルを更新できます。たとえば、MySQL を使用する場合は、`.env` 構成ファイルの `DB_*` 変数を次のように更新します。

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite 以外のデータベースの使用を選択した場合は、データベースを作成し、アプリケーションの [データベースの移行](/docs/{{version}}/migrations) を実行する必要があります。

```shell
php artisan migrate
```

> [!NOTE]
> macOS または Windows で開発していて、MySQL、PostgreSQL、または Redis をローカルにインストールする必要がある場合は、[ハードプロ](https://herd.laravel.com/#plans) または [DBngin](https://dbngin.com/) の使用を検討してください。

<a name="directory-configuration"></a>
### ディレクトリ構成

Laravel は常に、Web サーバーに設定された「Web ディレクトリ」のルートから提供される必要があります。 「Web ディレクトリ」のサブディレクトリから Laravel アプリケーションを提供しようとしないでください。これを試みると、アプリケーション内に存在する機密ファイルが公開される可能性があります。

<a name="installation-using-herd"></a>
## Herd を使用したインストール (Installation Using Herd)

[LaravelのHerd](https://herd.laravel.com) は、macOS および Windows 用の非常に高速なネイティブ Laravel および PHP 開発環境です。 Herd には、PHP や Nginx など、Laravel 開発を始めるために必要なものがすべて含まれています。

Herd をインストールしたら、Laravel を使用して開発を開始する準備が整います。 Herd には、`php`、`composer`、`laravel`、`expose`、`node`、`npm`、および `nvm` のコマンド ライン ツールが含まれています。

> [!NOTE]
> [ハードプロ](https://herd.laravel.com/#plans) は、ローカルの MySQL、Postgres、Redis データベースの作成と管理、ローカル メールの表示とログの監視などの強力な機能を追加して Herd を強化します。

<a name="herd-on-macos"></a>
### macOS 上のHerd

macOS で開発する場合は、[Herdのウェブサイト](https://herd.laravel.com) から Herd インストーラーをダウンロードできます。インストーラーは最新バージョンの PHP を自動的にダウンロードし、常にバックグラウンドで [Nginx](https://www.nginx.com/) を実行するように Mac を設定します。

Herd for macOS は、[dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) を使用して「パーク」ディレクトリをサポートします。パークディレクトリ内の Laravel アプリケーションはすべて、Herd によって自動的に提供されます。デフォルトでは、Herd は `~/Herd` にパークディレクトリを作成し、そのディレクトリ名を使用して、`.test` ドメイン上のこのディレクトリ内の任意の Laravel アプリケーションにアクセスできます。

Herd をインストールした後、新しい Laravel アプリケーションを作成する最も早い方法は、Herd にバンドルされている Laravel CLI を使用することです。

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

もちろん、システム トレイの Herd メニューから開くことができる Herd の UI を介して、パークしたディレクトリやその他の PHP 設定をいつでも管理できます。

Herd について詳しくは、[Herdのドキュメント](https://herd.laravel.com/docs) をご覧ください。

<a name="herd-on-windows"></a>
### Windows 上のHerd

Herd の Windows インストーラーは、[Herdのウェブサイト](https://herd.laravel.com/windows) からダウンロードできます。インストールが完了したら、Herd を起動してオンボーディング プロセスを完了し、Herd UI に初めてアクセスできます。

Herd UI には、Herd のシステム トレイ アイコンを左クリックしてアクセスできます。右クリックするとクイック メニューが開き、日常的に必要なすべてのツールにアクセスできます。

インストール中に、Herd は `%USERPROFILE%\Herd` のホーム ディレクトリに「パーク」ディレクトリを作成します。パークされたディレクトリ内のすべての Laravel アプリケーションは、Herd によって自動的に提供され、ディレクトリ名を使用して、`.test` ドメイン上のこのディレクトリ内のすべての Laravel アプリケーションにアクセスできます。

Herd をインストールした後、新しい Laravel アプリケーションを作成する最も早い方法は、Herd にバンドルされている Laravel CLI を使用することです。まず、Powershell を開いて次のコマンドを実行します。

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Herd について詳しくは、[Windows 用の Herd ドキュメント](https://herd.laravel.com/docs/windows) をご覧ください。

<a name="ide-support"></a>
## IDEのサポート (IDE Support)

Laravelアプリケーションを開発する際には、任意のコードエディタを自由に使用できます。軽量で拡張可能なエディターをお探しの場合は、[VSコード](https://code.visualstudio.com) または [Cursor](https://cursor.com) と公式 [Laravel VS コード拡張機能](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel) を組み合わせると、構文の強調表示、スニペット、Artisan コマンドの統合、Eloquent モデル、ルート、ミドルウェア、アセット、構成、および Inertia.js のスマート オートコンプリートなどの機能を備えた優れた Laravel サポートが提供されます。

Laravel の広範囲かつ堅牢なサポートについては、JetBrains IDE の [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025) をご覧ください。 PhpStorm の組み込み Laravel フレームワーク サポートには、Blade テンプレート、Eloquent モデルのスマート オートコンプリート、ルート、ビュー、翻訳、コンポーネントに加えて、強力なコード生成と Laravel プロジェクト全体のナビゲーションが含まれます。

クラウドベースの開発エクスペリエンスを求める人のために、[Firebase スタジオ](https://firebase.studio/) を使用すると、ブラウザーで直接 Laravel を使用して構築するための即時アクセスが提供されます。 Firebase Studio を使用すると、セットアップが不要で、どのデバイスからでも簡単に Laravel アプリケーションの構築を開始できます。

<a name="laravel-and-ai"></a>
## LaravelとAI (Laravel and AI)

[Laravelブースト](https://github.com/laravel/boost) は、AI コーディング エージェントと Laravel アプリケーションの間のギャップを埋める強力なツールです。 Boost は、AI エージェントに Laravel 固有のコンテキスト、ツール、ガイドラインを提供するため、Laravel の規則に従って、より正確なバージョン固有のコードを生成できます。

Laravel アプリケーションに Boost をインストールすると、AI エージェントは、使用しているパッケージの把握、データベースのクエリ、Laravel ドキュメントの検索、ブラウザのログの読み取り、テストの生成、Tinker 経由のコードの実行など、15 を超える特殊なツールにアクセスできるようになります。

さらに、Boost を使用すると、AI エージェントは、インストールされているパッケージのバージョンに応じて、17,000 を超えるベクトル化された Laravel エコシステム ドキュメントにアクセスできるようになります。これは、エージェントがプロジェクトで使用する正確なバージョンを対象としたガイダンスを提供できることを意味します。

Boost には、エージェントがフレームワークの規則に従い、適切なテストを作成し、Laravel コードを生成するときによくある落とし穴を回避するのに役立つ、Laravel が管理する AI ガイドラインも含まれています。

<a name="installing-laravel-boost"></a>
### Laravel Boostのインストール

Boost は、PHP 8.1 以降を実行している Laravel 10、11、12、13 アプリケーションにインストールできます。まず、Boost を開発依存関係としてインストールします。

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

<a name="adding-custom-ai-guidelines"></a>
#### カスタム AI ガイドラインの追加

独自のカスタム AI ガイドラインで Laravel Boost を拡張するには、`.blade.php` または `.md` ファイルをアプリケーションの `.ai/guidelines/*` ディレクトリに追加します。これらのファイルは、`boost:install` を実行すると、Laravel Boost のガイドラインに自動的に組み込まれます。

<a name="next-steps"></a>
## 次のステップ (Next Steps)

Laravel アプリケーションを作成したので、次に何を学べばよいのか疑問に思っているかもしれません。まず、次のドキュメントを読んで、Laravel がどのように動作するかを理解することを強くお勧めします。

<div class="content-list" markdown="1">

- [リクエストのライフサイクル](/docs/{{version}}/lifecycle)
- [Configuration](/docs/{{version}}/configuration)
- [ディレクトリ構造](/docs/{{version}}/structure)
- [Frontend](/docs/{{version}}/frontend)
- [サービスコンテナ](/docs/{{version}}/container)
- [Facades](/docs/{{version}}/facades)

</div>

Laravel をどのように使用したいかによって、旅の次のステップも決まります。 Laravel を使用するにはさまざまな方法がありますが、以下ではフレームワークの 2 つの主な使用例を検討します。

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


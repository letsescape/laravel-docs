# ディレクトリ構造 (Directory Structure)

- [Introduction](#introduction)
- [ルートディレクトリ](#the-root-directory)
    - [`app` ディレクトリ](#the-root-app-directory)
    - [`bootstrap` ディレクトリ](#the-bootstrap-directory)
    - [`config` ディレクトリ](#the-config-directory)
    - [`database` ディレクトリ](#the-database-directory)
    - [`lang` ディレクトリ](#the-lang-directory)
    - [`public` ディレクトリ](#the-public-directory)
    - [`resources` ディレクトリ](#the-resources-directory)
    - [`routes` ディレクトリ](#the-routes-directory)
    - [`storage` ディレクトリ](#the-storage-directory)
    - [`tests` ディレクトリ](#the-tests-directory)
    - [`vendor` ディレクトリ](#the-vendor-directory)
- [アプリディレクトリ](#the-app-directory)
    - [`Broadcasting` ディレクトリ](#the-broadcasting-directory)
    - [`Console` ディレクトリ](#the-console-directory)
    - [`Events` ディレクトリ](#the-events-directory)
    - [`Exceptions` ディレクトリ](#the-exceptions-directory)
    - [`Http` ディレクトリ](#the-http-directory)
    - [`Jobs` ディレクトリ](#the-jobs-directory)
    - [`Listeners` ディレクトリ](#the-listeners-directory)
    - [`Mail` ディレクトリ](#the-mail-directory)
    - [`Models` ディレクトリ](#the-models-directory)
    - [`Notifications` ディレクトリ](#the-notifications-directory)
    - [`Policies` ディレクトリ](#the-policies-directory)
    - [`Providers` ディレクトリ](#the-providers-directory)
    - [`Rules` ディレクトリ](#the-rules-directory)

<a name="introduction"></a>
## 導入 (Introduction)

デフォルトの Laravel アプリケーション構造は、大規模なアプリケーションと小規模なアプリケーションの両方に優れた出発点を提供することを目的としています。ただし、アプリケーションを自由に編成できます。 Laravel では、Composer がクラスを自動ロードできる限り、特定のクラスの配置場所にほとんど制限がありません。

> **注記**
> Laravel は初めてですか?最初の Laravel アプリケーションを構築する手順を説明しながら、フレームワークの実践的なツアーについては、[Laravelブートキャンプ](https://bootcamp.laravel.com) をご覧ください。

<a name="the-root-directory"></a>
## ルートディレクトリ (The Root Directory)

<a name="the-root-app-directory"></a>
#### アプリディレクトリ

`app` ディレクトリには、アプリケーションのコア コードが含まれています。このディレクトリについては、後ほど詳しく説明します。ただし、アプリケーション内のほとんどすべてのクラスはこのディレクトリにあります。

<a name="the-bootstrap-directory"></a>
#### ブートストラップ ディレクトリ

`bootstrap` ディレクトリには、フレームワークをブートストラップする `app.php` ファイルが含まれています。このディレクトリには、ルート キャッシュ ファイルやサービス キャッシュ ファイルなど、パフォーマンスを最適化するためにフレームワークで生成されたファイルが含まれる `cache` ディレクトリも格納されます。通常、このディレクトリ内のファイルを変更する必要はありません。

<a name="the-config-directory"></a>
#### 構成ディレクトリ

`config` ディレクトリには、名前が示すように、アプリケーションのすべての構成ファイルが含まれています。これらのファイルをすべて読んで、利用可能なすべてのオプションをよく理解することをお勧めします。

<a name="the-database-directory"></a>
#### データベースディレクトリ

`database` ディレクトリには、データベースの移行、モデル ファクトリ、およびシードが含まれています。必要に応じて、このディレクトリを使用して SQLite データベースを保持することもできます。

<a name="the-lang-directory"></a>
#### ラングディレクトリ

`lang` ディレクトリには、アプリケーションのすべての言語ファイルが格納されます。

<a name="the-public-directory"></a>
#### パブリックディレクトリ

`public` ディレクトリには、アプリケーションに入るすべてのリクエストのエントリ ポイントとなり、自動ロードを構成する `index.php` ファイルが含まれています。このディレクトリには、画像、JavaScript、CSS などのアセットも格納されます。

<a name="the-resources-directory"></a>
#### リソースディレクトリ

`resources` ディレクトリには、[views](/docs/{{version}}/views) と、CSS や JavaScript などの生の未コンパイル アセットが含まれています。

<a name="the-routes-directory"></a>
#### ルートディレクトリ

`routes` ディレクトリには、アプリケーションのすべてのルート定義が含まれています。デフォルトでは、Laravel にはいくつかのルートファイル (`web.php`、`api.php`、`console.php`、`channels.php`) が含まれています。

`web.php` ファイルには、`RouteServiceProvider` が `web` ミドルウェア グループに配置するルートが含まれており、セッション状態、CSRF 保護、Cookie 暗号化が提供されます。アプリケーションがステートレスな RESTful API を提供していない場合は、すべてのルートが `web.php` ファイルで定義される可能性が高くなります。

`api.php` ファイルには、`RouteServiceProvider` が `api` ミドルウェア グループに配置するルートが含まれています。これらのルートはステートレスであることを目的としているため、これらのルートを介してアプリケーションに入るリクエストは [トークン経由](/docs/{{version}}/sanctum) で認証されることを目的としており、セッション状態にはアクセスできません。

`console.php` ファイルでは、クロージャ ベースのコンソール コマンドをすべて定義できます。各クロージャはコマンド インスタンスにバインドされており、各コマンドの IO メソッドと対話する簡単なアプローチが可能になります。このファイルは HTTP ルートを定義しませんが、アプリケーションへのコンソール ベースのエントリ ポイント (ルート) を定義します。

`channels.php` ファイルには、アプリケーションがサポートするすべての [イベント放送](/docs/{{version}}/broadcasting) チャネルを登録できます。

<a name="the-storage-directory"></a>
#### ストレージディレクトリ

`storage` ディレクトリには、ログ、コンパイルされた Blade テンプレート、ファイル ベースのセッション、ファイル キャッシュ、およびフレームワークによって生成されたその他のファイルが含まれています。このディレクトリは、`app`、`framework`、および `logs` ディレクトリに分離されています。 `app` ディレクトリは、アプリケーションによって生成されたファイルを保存するために使用できます。 `framework` ディレクトリは、フレームワークで生成されたファイルとキャッシュを保存するために使用されます。最後に、`logs` ディレクトリにはアプリケーションのログ ファイルが含まれます。

`storage/app/public` ディレクトリは、プロファイル アバターなど、パブリックにアクセスできる必要があるユーザー生成ファイルを保存するために使用できます。このディレクトリを指すシンボリック リンクを `public/storage` に作成する必要があります。 `php artisan storage:link` Artisan コマンドを使用してリンクを作成できます。

<a name="the-tests-directory"></a>
#### テストディレクトリ

`tests` ディレクトリには自動テストが含まれています。 [PHPUnit](https://phpunit.de/) の単体テストと機能テストの例は、すぐに使用できるように提供されています。各テスト クラスには、`Test` という語の接尾辞を付ける必要があります。 `phpunit` または `php vendor/bin/phpunit` コマンドを使用してテストを実行できます。または、テスト結果をより詳細に美しく表現したい場合は、`php artisan test` Artisan コマンドを使用してテストを実行できます。

<a name="the-vendor-directory"></a>
#### ベンダーディレクトリ

`vendor` ディレクトリには、[Composer](https://getcomposer.org) 依存関係が含まれています。

<a name="the-app-directory"></a>
## アプリディレクトリ (The App Directory)

アプリケーションの大部分は、`app` ディレクトリに格納されています。デフォルトでは、このディレクトリは `App` の下に名前空間が設定されており、[PSR-4オートローディング規格](https://www.php-fig.org/psr/psr-4/) を使用して Composer によって自動ロードされます。

`app` ディレクトリには、`Console`、`Http`、`Providers` などのさまざまな追加ディレクトリが含まれています。 `Console` ディレクトリと `Http` ディレクトリは、アプリケーションのコアに API を提供すると考えてください。 HTTP プロトコルと CLI はどちらもアプリケーションと対話するメカニズムですが、実際にはアプリケーション ロジックは含まれません。言い換えれば、これらはアプリケーションにコマンドを発行する 2 つの方法です。 `Console` ディレクトリにはすべての Artisan コマンドが含まれ、`Http` ディレクトリにはコントローラ、ミドルウェア、リクエストが含まれます。

`make` Artisan コマンドを使用してクラスを生成すると、`app` ディレクトリ内に他のさまざまなディレクトリが生成されます。したがって、たとえば、`app/Jobs` ディレクトリは、`make:job` Artisan コマンドを実行してジョブ クラスを生成するまで存在しません。

> **注記**
> `app` ディレクトリ内のクラスの多くは、Artisan がコマンドを使用して生成できます。使用可能なコマンドを確認するには、ターミナルで `php artisan list make` コマンドを実行します。

<a name="the-broadcasting-directory"></a>
#### 放送ディレクトリ

`Broadcasting` ディレクトリには、アプリケーションのすべてのブロードキャスト チャネル クラスが含まれています。これらのクラスは、`make:channel` コマンドを使用して生成されます。このディレクトリはデフォルトでは存在しませんが、最初のチャネルを作成するときに作成されます。チャネルの詳細については、[イベント放送](/docs/{{version}}/broadcasting) のドキュメントを参照してください。

<a name="the-console-directory"></a>
#### コンソールディレクトリ

`Console` ディレクトリには、アプリケーションのカスタム Artisan コマンドがすべて含まれています。これらのコマンドは、`make:command` コマンドを使用して生成できます。このディレクトリには、コンソール カーネルも格納されます。ここにカスタム Artisan コマンドが登録され、[スケジュールされたタスク](/docs/{{version}}/scheduling) が定義されます。

<a name="the-events-directory"></a>
#### イベントディレクトリ

このディレクトリはデフォルトでは存在しませんが、`event:generate` および `make:event` Artisan コマンドによって作成されます。 `Events` ディレクトリには [イベントクラス](/docs/{{version}}/events) が含まれています。イベントを使用して、特定のアクションが発生したことをアプリケーションの他の部分に警告することができ、大幅な柔軟性と分離が実現します。

<a name="the-exceptions-directory"></a>
#### 例外ディレクトリ

`Exceptions` ディレクトリにはアプリケーションの例外ハンドラーが含まれており、アプリケーションによってスローされた例外を配置するのにも適した場所です。例外のログ記録または表示方法をカスタマイズしたい場合は、このディレクトリ内の `Handler` クラスを変更する必要があります。

<a name="the-http-directory"></a>
#### HTTP ディレクトリ

`Http` ディレクトリには、コントローラ、ミドルウェア、フォーム リクエストが含まれています。アプリケーションに入るリクエストを処理するロジックのほとんどは、このディレクトリに配置されます。

<a name="the-jobs-directory"></a>
#### 求人ディレクトリ

このディレクトリはデフォルトでは存在しませんが、`make:job` Artisan コマンドを実行すると作成されます。 `Jobs` ディレクトリには、アプリケーションの [キュー可能なジョブ](/docs/{{version}}/queues) が格納されます。ジョブはアプリケーションによってキューに入れられるか、現在のリクエストのライフサイクル内で同期的に実行されます。現在のリクエスト中に同期的に実行されるジョブは、[コマンドパターン](https://en.wikipedia.org/wiki/Command_pattern) の実装であるため、「コマンド」と呼ばれることがあります。

<a name="the-listeners-directory"></a>
#### リスナディレクトリ

このディレクトリはデフォルトでは存在しませんが、`event:generate` または `make:listener` Artisan コマンドを実行すると作成されます。 `Listeners` ディレクトリには、[events](/docs/{{version}}/events) を処理するクラスが含まれています。イベント リスナはイベント インスタンスを受信し、発生したイベントに応答してロジックを実行します。たとえば、`UserRegistered` イベントは、`SendWelcomeEmail` リスナによって処理される場合があります。

<a name="the-mail-directory"></a>
#### メールディレクトリ

このディレクトリはデフォルトでは存在しませんが、`make:mail` Artisan コマンドを実行すると作成されます。 `Mail` ディレクトリには、アプリケーションによって送信されたすべての [電子メールを表すクラス](/docs/{{version}}/mail) が含まれています。メール オブジェクトを使用すると、電子メールを構築するすべてのロジックを、`Mail::send` メソッドを使用して送信できる単一の単純なクラスにカプセル化できます。

<a name="the-models-directory"></a>
#### モデルディレクトリ

`Models` ディレクトリには、[Eloquent モデルクラス](/docs/{{version}}/eloquent) のすべてが含まれています。 Laravel に含まれる Eloquent ORM は、データベースを操作するための美しくシンプルな ActiveRecord 実装を提供します。各データベース テーブルには、そのテーブルと対話するために使用される対応する「モデル」があります。モデルを使用すると、テーブル内のデータをクエリしたり、テーブルに新しいレコードを挿入したりできます。

<a name="the-notifications-directory"></a>
#### 通知ディレクトリ

このディレクトリはデフォルトでは存在しませんが、`make:notification` Artisan コマンドを実行すると作成されます。 `Notifications` ディレクトリには、アプリケーション内で発生するイベントに関する単純な通知など、アプリケーションによって送信されるすべての「トランザクション」[notifications](/docs/{{version}}/notifications) が含まれています。 Laravel の通知機能は、電子メール、Slack、SMS などのさまざまなドライバを介した、またはデータベースに保存された通知の送信を抽象化します。

<a name="the-policies-directory"></a>
#### ポリシーディレクトリ

このディレクトリはデフォルトでは存在しませんが、`make:policy` Artisan コマンドを実行すると作成されます。 `Policies` ディレクトリには、アプリケーションの [認可ポリシークラス](/docs/{{version}}/authorization) が含まれています。ポリシーは、ユーザーがリソースに対して特定のアクションを実行できるかどうかを決定するために使用されます。

<a name="the-providers-directory"></a>
#### プロバイダ ディレクトリ

`Providers` ディレクトリには、アプリケーションのすべての [サービスプロバイダ](/docs/{{version}}/providers) が含まれています。サービスプロバイダは、サービスコンテナーにサービスをバインドしたり、イベントを登録したり、その他のタスクを実行して、アプリケーションを受信リクエストに備えて準備したりすることによって、アプリケーションをブートストラップします。

新しい Laravel アプリケーションでは、このディレクトリにはすでに複数のプロバイダが含まれています。必要に応じて、このディレクトリに独自のプロバイダを自由に追加できます。

<a name="the-rules-directory"></a>
#### ルールディレクトリ

このディレクトリはデフォルトでは存在しませんが、`make:rule` Artisan コマンドを実行すると作成されます。 `Rules` ディレクトリには、アプリケーションのカスタム検証ルール オブジェクトが含まれています。ルールは、複雑な検証ロジックを単純なオブジェクトにカプセル化するために使用されます。詳細については、[検証ドキュメント](/docs/{{version}}/validation) をご覧ください。


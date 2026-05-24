# 構成 (Configuration)

- [Introduction](#introduction)
- [環境構成](#environment-configuration)
    - [環境変数のタイプ](#environment-variable-types)
    - [環境設定の取得](#retrieving-environment-configuration)
    - [現在の環境を判断する](#determining-the-current-environment)
    - [環境ファイルの暗号化](#encrypting-environment-files)
- [構成値へのアクセス](#accessing-configuration-values)
- [構成のキャッシュ](#configuration-caching)
- [デバッグモード](#debug-mode)
- [メンテナンスモード](#maintenance-mode)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel フレームワークの構成ファイルはすべて、`config` ディレクトリに保存されます。各オプションは文書化されているので、ファイルに目を通して、利用可能なオプションをよく理解してください。

これらの構成ファイルを使用すると、データベース接続情報、メール サーバー情報に加え、アプリケーションのタイムゾーンや暗号化キーなどのその他のさまざまなコア構成値などを構成できます。

<a name="application-overview"></a>
#### アプリケーションの概要

お急ぎですか？ `about` Artisan コマンドを使用して、アプリケーションの構成、ドライバ、および環境の概要を簡単に取得できます。

```shell
php artisan about
```

アプリケーション概要出力の特定のセクションのみに興味がある場合は、`--only` オプションを使用してそのセクションをフィルターできます。

```shell
php artisan about --only=environment
```

<a name="environment-configuration"></a>
## 環境構成 (Environment Configuration)

多くの場合、アプリケーションが実行されている環境に基づいて異なる構成値を使用すると便利です。たとえば、運用サーバーとは異なるキャッシュ ドライバをローカルで使用したい場合があります。

これを簡単にするために、Laravel は [DotEnv](https://github.com/vlucas/phpdotenv) PHP ライブラリを利用します。 Laravel を新規インストールすると、アプリケーションのルート ディレクトリに、多くの一般的な環境変数を定義する `.env.example` ファイルが含まれます。 Laravel のインストールプロセス中に、このファイルは自動的に `.env` にコピーされます。

Laravel のデフォルトの `.env` ファイルには、アプリケーションがローカルで実行されているか実稼働 Web サーバーで実行されているかによって異なる可能性があるいくつかの一般的な構成値が含まれています。これらの値は、Laravel の `env` 関数を使用して、`config` ディレクトリ内のさまざまな Laravel 構成ファイルから取得されます。

チームで開発している場合は、引き続き `.env.example` ファイルをアプリケーションに含めることをお勧めします。サンプル構成ファイルにプレースホルダー値を入れることで、チームの他の開発者は、アプリケーションの実行にどの環境変数が必要かを明確に確認できます。

> **注記**
> `.env` ファイル内の変数は、サーバー レベルまたはシステム レベルの環境変数などの外部環境変数によってオーバーライドできます。

<a name="environment-file-security"></a>
#### 環境ファイルのセキュリティ

アプリケーションを使用する各開発者/サーバーは異なる環境構成を必要とする可能性があるため、`.env` ファイルをアプリケーションのソース管理にコミットしないでください。さらに、侵入者がソース管理リポジトリにアクセスした場合、機密の資格情報が漏洩してしまうため、セキュリティ リスクとなります。

ただし、Laravel の組み込み [環境の暗号化](#encrypting-environment-files) を使用して環境ファイルを暗号化することは可能です。暗号化された環境ファイルはソース管理に安全に配置できます。

<a name="additional-environment-files"></a>
#### 追加の環境ファイル

アプリケーションの環境変数をロードする前に、Laravel は、`APP_ENV` 環境変数が外部から提供されているかどうか、または `--env` CLI 引数が指定されているかどうかを判断します。その場合、Laravel は `.env.[APP_ENV]` ファイルが存在する場合、そのファイルをロードしようとします。存在しない場合は、デフォルトの `.env` ファイルがロードされます。

<a name="environment-variable-types"></a>
### 環境変数のタイプ

`.env` ファイル内のすべての変数は通常、文字列として解析されるため、`env()` 関数からより広範囲の型を返すことができるように、いくつかの予約値が作成されています。

| `.env` 値 | `env()` 値 |
|--------------|---------------|
| 真実         | (ブール値) true   |
| （真実）       | (ブール値) true   |
| 間違い        | (ブール値) false  |
| （間違い）      | (ブール値) false  |
| 空の        | （弦） ''   |
| （空の）      | （弦） ''   |
| ヌル         | (ヌル)ヌル   |
| (ヌル)       | (ヌル)ヌル   |

スペースを含む値を使用して環境変数を定義する必要がある場合は、値を二重引用符で囲むことで定義できます。

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 環境設定の取得

`.env` ファイルにリストされているすべての変数は、アプリケーションがリクエストを受信すると、`$_ENV` PHP スーパーグローバルにロードされます。ただし、`env` 関数を使用して、構成ファイル内のこれらの変数から値を取得することもできます。実際、Laravel 設定ファイルを確認すると、多くのオプションがすでにこの関数を使用していることがわかります。

    'debug' => env('APP_DEBUG', false),

`env` 関数に渡される 2 番目の値は「デフォルト値」です。指定されたキーに環境変数が存在しない場合、この値が返されます。

<a name="determining-the-current-environment"></a>
### 現在の環境を判断する

現在のアプリケーション環境は、`.env` ファイルの `APP_ENV` 変数によって決定されます。この値には、`App` [facade](/docs/{{version}}/facades) の `environment` メソッドを介してアクセスできます。

    use Illuminate\Support\Facades\App;

    $environment = App::environment();

`environment` メソッドに引数を渡して、環境が指定された値と一致するかどうかを判断することもできます。環境が指定された値のいずれかに一致する場合、メソッドは `true` を返します。

    if (App::environment('local')) {
        // The environment is local
    }

    if (App::environment(['local', 'staging'])) {
        // The environment is either local OR staging...
    }

> **注記**
> 現在のアプリケーション環境の検出は、サーバーレベルの `APP_ENV` 環境変数を定義することで上書きできます。

<a name="encrypting-environment-files"></a>
### 環境ファイルの暗号化

暗号化されていない環境ファイルはソース管理に保存しないでください。ただし、Laravel を使用すると、環境ファイルを暗号化して、アプリケーションの残りの部分とともにソース管理に安全に追加できるようになります。

<a name="encryption"></a>
#### 暗号化

環境ファイルを暗号化するには、`env:encrypt` コマンドを使用できます。

```shell
php artisan env:encrypt
```

`env:encrypt` コマンドを実行すると、`.env` ファイルが暗号化され、暗号化されたコンテンツが `.env.encrypted` ファイルに配置されます。復号化キーはコマンドの出力に表示され、安全なパスワード マネージャーに保存する必要があります。独自の暗号化キーを提供したい場合は、コマンドを呼び出すときに `--key` オプションを使用できます。

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> **注記**
> 提供されるキーの長さは、使用されている暗号化方式で必要なキーの長さと一致する必要があります。デフォルトでは、Laravel は 32 文字のキーを必要とする `AES-256-CBC` 暗号を使用します。コマンドを呼び出すときに `--cipher` オプションを渡すことで、Laravel の [encrypter](/docs/{{version}}/encryption) でサポートされている暗号を自由に使用できます。

アプリケーションに `.env` や `.env.staging` などの複数の環境ファイルがある場合は、`--env` オプションで環境名を指定することで、暗号化する環境ファイルを指定できます。

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 復号化

環境ファイルを復号化するには、`env:decrypt` コマンドを使用できます。このコマンドには、Laravel が `LARAVEL_ENV_ENCRYPTION_KEY` 環境変数から取得する復号キーが必要です。

```shell
php artisan env:decrypt
```

または、`--key` オプションを使用してキーをコマンドに直接指定することもできます。

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` コマンドが呼び出されると、Laravel は `.env.encrypted` ファイルの内容を復号化し、復号化された内容を `.env` ファイルに配置します。

カスタム暗号化暗号を使用するために、`--cipher` オプションを `env:decrypt` コマンドに指定できます。

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

アプリケーションに `.env` や `.env.staging` などの複数の環境ファイルがある場合は、`--env` オプションで環境名を指定することで、復号化する環境ファイルを指定できます。

```shell
php artisan env:decrypt --env=staging
```

既存の環境ファイルを上書きするには、`--force` オプションを `env:decrypt` コマンドに指定します。

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 構成値へのアクセス (Accessing Configuration Values)

グローバル `config` 関数を使用すると、アプリケーションのどこからでも構成値に簡単にアクセスできます。設定値には、アクセスするファイル名とオプションを含む「ドット」構文を使用してアクセスできます。デフォルト値を指定することもでき、構成オプションが存在しない場合はデフォルト値が返されます。

    $value = config('app.timezone');

    // Retrieve a default value if the configuration value does not exist...
    $value = config('app.timezone', 'Asia/Seoul');

実行時に構成値を設定するには、配列を `config` 関数に渡します。

    config(['app.timezone' => 'America/Chicago']);

<a name="configuration-caching"></a>
## 構成のキャッシュ (Configuration Caching)

アプリケーションの速度を向上させるには、`config:cache` Artisan コマンドを使用して、すべての構成ファイルを 1 つのファイルにキャッシュする必要があります。これにより、アプリケーションのすべての構成オプションが 1 つのファイルに結合され、フレームワークによってすぐにロードできるようになります。

通常、実稼働デプロイメント・プロセスの一部として `php artisan config:cache` コマンドを実行する必要があります。アプリケーションの開発中に構成オプションを頻繁に変更する必要があるため、ローカル開発中にこのコマンドを実行しないでください。

`config:clear` コマンドを使用して、キャッシュされた構成を削除できます。

```shell
php artisan config:clear
```

> **警告**
> デプロイメントプロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされません。したがって、`env` 関数は、外部のシステム レベルの環境変数のみを返します。

<a name="debug-mode"></a>
## デバッグモード (Debug Mode)

`config/app.php` 構成ファイルの `debug` オプションは、エラーに関する情報が実際にユーザーに表示される量を決定します。デフォルトでは、このオプションは、`.env` ファイルに保存されている `APP_DEBUG` 環境変数の値を尊重するように設定されています。

ローカル開発の場合は、`APP_DEBUG` 環境変数を `true` に設定する必要があります。 **実稼働環境では、この値は常に `false` である必要があります。運用環境で変数が `true` に設定されている場合、機密の構成値がアプリケーションのエンド ユーザーに公開される危険があります。**

<a name="maintenance-mode"></a>
## メンテナンスモード (Maintenance Mode)

アプリケーションがメンテナンス モードの場合、アプリケーションへのすべてのリクエストに対してカスタム ビューが表示されます。これにより、更新中またはメンテナンスの実行中にアプリケーションを簡単に「無効化」できます。メンテナンス モード チェックは、アプリケーションのデフォルトのミドルウェア スタックに含まれています。アプリケーションがメンテナンス モードの場合、`Symfony\Component\HttpKernel\Exception\HttpException` インスタンスがステータス コード 503 でスローされます。

メンテナンス モードを有効にするには、`down` Artisan コマンドを実行します。

```shell
php artisan down
```

すべてのメンテナンス モード応答とともに `Refresh` HTTP ヘッダーを送信したい場合は、`down` コマンドを呼び出すときに `refresh` オプションを指定できます。 `Refresh` ヘッダーは、指定された秒数の後にページを自動的に更新するようにブラウザーに指示します。

```shell
php artisan down --refresh=15
```

`retry` オプションを `down` コマンドに指定することもできます。これは、`Retry-After` HTTP ヘッダーの値として設定されますが、通常、ブラウザーはこのヘッダーを無視します。

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### メンテナンスモードのバイパス

シークレット トークンを使用してメンテナンス モードをバイパスできるようにするには、`secret` オプションを使用してメンテナンス モード バイパス トークンを指定できます。

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

アプリケーションをメンテナンス モードにした後、このトークンに一致するアプリケーション URL に移動すると、Laravel はブラウザにメンテナンス モード バイパス Cookie を発行します。

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

この非表示のルートにアクセスすると、アプリケーションの `/` ルートにリダイレクトされます。ブラウザに Cookie が発行されると、メンテナンス モードでないかのようにアプリケーションを通常どおり閲覧できるようになります。

> **注記**
> メンテナンス モードのシークレットは通常、英数字と、必要に応じてダッシュで構成されます。 URL では、`?` や `&` などの特別な意味を持つ文字を使用しないでください。

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### メンテナンス モード ビューのプリレンダリング

デプロイメント中に `php artisan down` コマンドを使用する場合でも、Composer の依存関係または他のインフラストラクチャ コンポーネントの更新中にユーザーがアプリケーションにアクセスすると、エラーが発生することがあります。これは、アプリケーションがメンテナンス モードであることを判断し、テンプレート エンジンを使用してメンテナンス モード ビューをレンダリングするために、Laravel フレームワークの重要な部分を起動する必要があるために発生します。

このため、Laravel では、リクエスト サイクルの最初に返されるメンテナンス モード ビューを事前にレンダリングできます。このビューは、アプリケーションの依存関係が読み込まれる前にレンダリングされます。 `down` コマンドの `render` オプションを使用して、選択したテンプレートを事前レンダリングできます。

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### メンテナンス モード リクエストのリダイレクト

メンテナンスモードの間、LaravelはユーザーがアクセスしようとしているすべてのアプリケーションURLに対してメンテナンスモードビューを表示します。必要に応じて、すべてのリクエストを特定の URL にリダイレクトするように Laravel に指示できます。これは、`redirect` オプションを使用して実現できます。たとえば、すべてのリクエストを `/` URI にリダイレクトしたい場合があります。

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### メンテナンスモードの無効化

メンテナンス モードを無効にするには、`up` コマンドを使用します。

```shell
php artisan up
```

> **注記**
> `resources/views/errors/503.blade.php` で独自のテンプレートを定義することで、デフォルトのメンテナンス モード テンプレートをカスタマイズできます。

<a name="maintenance-mode-queues"></a>
#### メンテナンスモードとキュー

アプリケーションがメンテナンス モードの間は、[キューに入れられたジョブ](/docs/{{version}}/queues) は処理されません。アプリケーションがメンテナンス モードを終了しても、ジョブは通常どおり処理され続けます。

<a name="alternatives-to-maintenance-mode"></a>
#### メンテナンスモードの代替手段

メンテナンスモードではアプリケーションに数秒のダウンタイムが必要なため、Laravel でゼロダウンタイムのデプロイメントを実現するには、[Laravel Vapor](https://vapor.laravel.com) や [Envoyer](https://envoyer.io) などの代替手段を検討してください。


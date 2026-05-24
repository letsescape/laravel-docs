# 郵便 (Mail)

- [Introduction](#introduction)
    - [Configuration](#configuration)
    - [ドライバの前提条件](#driver-prerequisites)
    - [フェイルオーバー構成](#failover-configuration)
- [メール可能ファイルの生成](#generating-mailables)
- [メール可能ファイルの作成](#writing-mailables)
    - [送信者の構成](#configuring-the-sender)
    - [ビューの構成](#configuring-the-view)
    - [データの表示](#view-data)
    - [Attachments](#attachments)
    - [インライン添付ファイル](#inline-attachments)
    - [取り付け可能なオブジェクト](#attachable-objects)
    - [Headers](#headers)
    - [タグとメタデータ](#tags-and-metadata)
    - [Symfony メッセージのカスタマイズ](#customizing-the-symfony-message)
- [マークダウン メール可能ファイル](#markdown-mailables)
    - [マークダウン メール可能ファイルの生成](#generating-markdown-mailables)
    - [マークダウンメッセージの作成](#writing-markdown-messages)
    - [コンポーネントのカスタマイズ](#customizing-the-components)
- [メールの送信](#sending-mail)
    - [メールのキューイング](#queueing-mail)
- [メール可能ファイルのレンダリング](#rendering-mailables)
    - [ブラウザでのメール可能ファイルのプレビュー](#previewing-mailables-in-the-browser)
- [メール可能ファイルのローカライズ](#localizing-mailables)
- [メール可能ファイルのテスト](#testing-mailables)
- [メールとローカル開発](#mail-and-local-development)
- [Events](#events)
- [カスタムトランスポート](#custom-transports)
    - [追加の Symfony トランスポート](#additional-symfony-transports)

<a name="introduction"></a>
## 導入 (Introduction)

電子メールの送信は複雑である必要はありません。 Laravel は、人気のある [Symfony Mailer](https://symfony.com/doc/6.0/mailer.html) コンポーネントを活用したクリーンでシンプルな電子メール API を提供します。 Laravel と Symfony Mailer は、SMTP、Mailgun、Postmark、Amazon SES、および `sendmail` 経由で電子メールを送信するためのドライバを提供しており、選択したローカルまたはクラウドベースのサービスを通じてメールの送信をすぐに開始できます。

<a name="configuration"></a>
### 構成

Laravel の電子メール サービスは、アプリケーションの `config/mail.php` 構成ファイルを介して構成できます。このファイル内で構成された各メーラーは、独自の固有の構成および独自の「トランスポート」さえ持つことができ、アプリケーションがさまざまな電子メール サービスを使用して特定の電子メール メッセージを送信できるようになります。たとえば、アプリケーションでは消印を使用してトランザクション E メールを送信し、Amazon SES を使用して一括 E メールを送信する場合があります。

`mail` 構成ファイル内に、`mailers` 構成配列があります。この配列には、Laravel でサポートされている主要なメールドライバ/トランスポートのそれぞれのサンプル構成エントリが含まれています。一方、`default` 構成値は、アプリケーションが電子メールメッセージを送信する必要があるときにデフォルトで使用されるメーラーを決定します。

<a name="driver-prerequisites"></a>
### ドライバ/トランスポートの前提条件

Mailgun や Postmark などの API ベースのドライバは、多くの場合、SMTP サーバー経由でメールを送信するよりも簡単で高速です。可能な限り、これらのドライバのいずれかを使用することをお勧めします。

<a name="mailgun-driver"></a>
#### メールガンドライバ

Mailgun ドライバを使用するには、Composer 経由で Symfony の Mailgun Mailer トランスポートをインストールします。

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

次に、アプリケーションの `config/mail.php` 構成ファイルの `default` オプションを `mailgun` に設定します。アプリケーションのデフォルトのメーラーを構成した後、`config/services.php` 構成ファイルに次のオプションが含まれていることを確認します。

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
    ],

米国の [メールガン地域](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions) を使用していない場合は、`services` 構成ファイルで地域のエンドポイントを定義できます。

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
        'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
    ],

<a name="postmark-driver"></a>
#### 消印ドライバ

Postmark ドライバを使用するには、Composer 経由で Symfony の Postmark Mailer トランスポートをインストールします。

```shell
composer require symfony/postmark-mailer symfony/http-client
```

次に、アプリケーションの `config/mail.php` 構成ファイルの `default` オプションを `postmark` に設定します。アプリケーションのデフォルトのメーラーを構成した後、`config/services.php` 構成ファイルに次のオプションが含まれていることを確認します。

    'postmark' => [
        'token' => env('POSTMARK_TOKEN'),
    ],

特定のメーラーで使用する消印メッセージ ストリームを指定したい場合は、メーラーの構成配列に `message_stream_id` 構成オプションを追加できます。この構成配列は、アプリケーションの `config/mail.php` 構成ファイルにあります。

    'postmark' => [
        'transport' => 'postmark',
        'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    ],

この方法では、異なるメッセージ ストリームを持つ複数の Postmark メーラーを設定することもできます。

<a name="ses-driver"></a>
#### SESドライバ

Amazon SES ドライバを使用するには、まず Amazon AWS SDK for PHP をインストールする必要があります。このライブラリは、Composer パッケージ マネージャーを介してインストールできます。

```shell
composer require aws/aws-sdk-php
```

次に、`config/mail.php` 構成ファイルの `default` オプションを `ses` に設定し、`config/services.php` 構成ファイルに次のオプションが含まれていることを確認します。

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    ],

セッション トークン経由で AWS [一時的な認証情報](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html) を利用するには、アプリケーションの SES 設定に `token` キーを追加します。

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
        'token' => env('AWS_SESSION_TOKEN'),
    ],

電子メールの送信時に Laravel が AWS SDK の `SendEmail` メソッドに渡す [追加オプション](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail) を定義したい場合は、`ses` 設定内で `options` 配列を定義できます。

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
        'options' => [
            'ConfigurationSetName' => 'MyConfigurationSet',
            'EmailTags' => [
                ['Name' => 'foo', 'Value' => 'bar'],
            ],
        ],
    ],

<a name="failover-configuration"></a>
### フェイルオーバー構成

場合によっては、アプリケーションのメールを送信するように構成した外部サービスがダウンしている可能性があります。このような場合、プライマリ配信ドライバがダウンした場合に使用されるバックアップ メール配信構成を 1 つ以上定義すると便利です。

これを実現するには、アプリケーションの `mail` 構成ファイル内で、`failover` トランスポートを使用するメーラーを定義する必要があります。アプリケーションの `failover` メーラーの構成配列には、配信用にメール ドライバを選択する順序を参照する `mailers` の配列が含まれている必要があります。

    'mailers' => [
        'failover' => [
            'transport' => 'failover',
            'mailers' => [
                'postmark',
                'mailgun',
                'sendmail',
            ],
        ],

        // ...
    ],

フェイルオーバー メーラーを定義したら、アプリケーションの `mail` 構成ファイル内の `default` 構成キーの値としてその名前を指定することにより、このメーラーをアプリケーションで使用されるデフォルトのメーラーとして設定する必要があります。

    'default' => env('MAIL_MAILER', 'failover'),

<a name="generating-mailables"></a>
## メール可能ファイルの生成 (Generating Mailables)

Laravel アプリケーションを構築する場合、アプリケーションによって送信される各種類の電子メールは、「メール可能」クラスとして表されます。これらのクラスは、`app/Mail` ディレクトリに保存されます。アプリケーションにこのディレクトリが表示されなくても心配する必要はありません。このディレクトリは、`make:mail` Artisan コマンドを使用して最初のメール可能クラスを作成するときに生成されるためです。

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## メール可能ファイルの作成 (Writing Mailables)

メール可能なクラスを生成したら、そのクラスを開いて、その内容を探索できるようにします。メール可能クラスの構成は、`envelope`、`content`、`attachments` メソッドなど、いくつかのメソッドで行われます。

`envelope` メソッドは、メッセージの件名と、場合によっては受信者を定義する `Illuminate\Mail\Mailables\Envelope` オブジェクトを返します。 `content` メソッドは、メッセージ コンテンツの生成に使用される [Blade テンプレート](/docs/{{version}}/blade) を定義する `Illuminate\Mail\Mailables\Content` オブジェクトを返します。

<a name="configuring-the-sender"></a>
### 送信者の構成

<a name="using-the-envelope"></a>
#### エンベロープの使用

まず、電子メールの送信者の構成を見てみましょう。言い換えれば、電子メールの「送信者」が誰になるのかということです。送信者を構成するには 2 つの方法があります。まず、メッセージのエンベロープに「差出人」アドレスを指定します。

    use Illuminate\Mail\Mailables\Address;
    use Illuminate\Mail\Mailables\Envelope;

    /**
     * Get the message envelope.
     *
     * @return \Illuminate\Mail\Mailables\Envelope
     */
    public function envelope()
    {
        return new Envelope(
            from: new Address('jeffrey@example.com', 'Jeffrey Way'),
            subject: 'Order Shipped',
        );
    }

必要に応じて、`replyTo` アドレスを指定することもできます。

    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        replyTo: [
            new Address('taylor@example.com', 'Taylor Otwell'),
        ],
        subject: 'Order Shipped',
    );

<a name="using-a-global-from-address"></a>
#### グローバル `from` アドレスの使用

ただし、アプリケーションがすべての電子メールに同じ「差出人」アドレスを使用する場合、生成する各メール可能クラスで `from` メソッドを呼び出すのが面倒になる可能性があります。代わりに、`config/mail.php` 構成ファイルでグローバル「送信元」アドレスを指定できます。このアドレスは、メール可能クラス内に他の「差出人」アドレスが指定されていない場合に使用されます。

    'from' => ['address' => 'example@example.com', 'name' => 'App Name'],

さらに、`config/mail.php` 構成ファイル内でグローバル「reply_to」アドレスを定義できます。

    'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],

<a name="configuring-the-view"></a>
### ビューの構成

メール可能クラスの `content` メソッド内で、`view`、または電子メールのコンテンツをレンダリングするときに使用するテンプレートを定義できます。通常、各電子メールは [Blade テンプレート](/docs/{{version}}/blade) を使用してコンテンツをレンダリングするため、電子メールの HTML を構築するときに、Blade テンプレート エンジンの能力と利便性を最大限に活用できます。

    /**
     * Get the message content definition.
     *
     * @return \Illuminate\Mail\Mailables\Content
     */
    public function content()
    {
        return new Content(
            view: 'emails.orders.shipped',
        );
    }

> **注記**
> すべての電子メール テンプレートを格納する `resources/views/emails` ディレクトリを作成することもできます。ただし、`resources/views` ディレクトリ内のどこにでも自由に配置できます。

<a name="plain-text-emails"></a>
#### プレーンテキストメール

電子メールのプレーンテキスト バージョンを定義したい場合は、メッセージの `Content` 定義を作成するときにプレーンテキスト テンプレートを指定できます。 `view` パラメータと同様に、`text` パラメータは、電子メールのコンテンツをレンダリングするために使用されるテンプレート名である必要があります。メッセージの HTML バージョンとプレーンテキスト バージョンの両方を自由に定義できます。

    /**
     * Get the message content definition.
     *
     * @return \Illuminate\Mail\Mailables\Content
     */
    public function content()
    {
        return new Content(
            view: 'emails.orders.shipped',
            text: 'emails.orders.shipped-text'
        );
    }

わかりやすくするために、`html` パラメーターは `view` パラメーターのエイリアスとして使用できます。

    return new Content(
        html: 'emails.orders.shipped',
        text: 'emails.orders.shipped-text'
    );

<a name="view-data"></a>
### データの表示

<a name="via-public-properties"></a>
#### 公共プロパティ経由

通常、電子メールの HTML をレンダリングするときに利用できるデータをビューに渡す必要があります。ビューでデータを利用できるようにするには 2 つの方法があります。まず、メール可能クラスで定義されたパブリック プロパティは自動的にビューで利用できるようになります。したがって、たとえば、メール可能クラスのコンストラクターにデータを渡し、そのデータをクラスで定義されたパブリック プロパティに設定できます。

    <?php

    namespace App\Mail;

    use App\Models\Order;
    use Illuminate\Bus\Queueable;
    use Illuminate\Mail\Mailable;
    use Illuminate\Mail\Mailables\Content;
    use Illuminate\Queue\SerializesModels;

    class OrderShipped extends Mailable
    {
        use Queueable, SerializesModels;

        /**
         * The order instance.
         *
         * @var \App\Models\Order
         */
        public $order;

        /**
         * Create a new message instance.
         *
         * @param  \App\Models\Order  $order
         * @return void
         */
        public function __construct(Order $order)
        {
            $this->order = $order;
        }

        /**
         * Get the message content definition.
         *
         * @return \Illuminate\Mail\Mailables\Content
         */
        public function content()
        {
            return new Content(
                view: 'emails.orders.shipped',
            );
        }
    }

データがパブリック プロパティに設定されると、そのデータは自動的にビューで使用できるようになり、Blade テンプレート内の他のデータにアクセスするのと同じようにアクセスできます。

    <div>
        Price: {{ $order->price }}
    </div>

<a name="via-the-with-parameter"></a>
#### `with` パラメータ経由:

テンプレートに送信される前に電子メールのデータの形式をカスタマイズしたい場合は、`Content` 定義の `with` パラメーターを介してデータをビューに手動で渡すことができます。通常は、メール可能クラスのコンストラクターを介してデータを渡します。ただし、データがテンプレートで自動的に使用可能にならないように、このデータを `protected` または `private` プロパティに設定する必要があります。

    <?php

    namespace App\Mail;

    use App\Models\Order;
    use Illuminate\Bus\Queueable;
    use Illuminate\Mail\Mailable;
    use Illuminate\Mail\Mailables\Content;
    use Illuminate\Queue\SerializesModels;

    class OrderShipped extends Mailable
    {
        use Queueable, SerializesModels;

        /**
         * The order instance.
         *
         * @var \App\Models\Order
         */
        protected $order;

        /**
         * Create a new message instance.
         *
         * @param  \App\Models\Order  $order
         * @return void
         */
        public function __construct(Order $order)
        {
            $this->order = $order;
        }

        /**
         * Get the message content definition.
         *
         * @return \Illuminate\Mail\Mailables\Content
         */
        public function content()
        {
            return new Content(
                view: 'emails.orders.shipped',
                with: [
                    'orderName' => $this->order->name,
                    'orderPrice' => $this->order->price,
                ],
            );
        }
    }

データが `with` メソッドに渡されると、そのデータはビューで自動的に使用可能になるため、Blade テンプレート内の他のデータにアクセスするのと同じようにアクセスできます。

    <div>
        Price: {{ $orderPrice }}
    </div>

<a name="attachments"></a>
### 添付ファイル

電子メールに添付ファイルを追加するには、メッセージの `attachments` メソッドによって返される配列に添付ファイルを追加します。まず、`Attachment` クラスによって提供される `fromPath` メソッドにファイル パスを指定して、添付ファイルを追加できます。

    use Illuminate\Mail\Mailables\Attachment;

    /**
     * Get the attachments for the message.
     *
     * @return \Illuminate\Mail\Mailables\Attachment[]
     */
    public function attachments()
    {
        return [
            Attachment::fromPath('/path/to/file'),
        ];
    }

メッセージにファイルを添付する場合、`as` および `withMime` メソッドを使用して、添付ファイルの表示名や MIME タイプを指定することもできます。

    /**
     * Get the attachments for the message.
     *
     * @return \Illuminate\Mail\Mailables\Attachment[]
     */
    public function attachments()
    {
        return [
            Attachment::fromPath('/path/to/file')
                    ->as('name.pdf')
                    ->withMime('application/pdf'),
        ];
    }

<a name="attaching-files-from-disk"></a>
#### ディスクからファイルを添付する

[ファイルシステムディスク](/docs/{{version}}/filesystem) のいずれかにファイルを保存している場合は、`fromStorage` 添付方法を使用してそのファイルを電子メールに添付できます。

    /**
     * Get the attachments for the message.
     *
     * @return \Illuminate\Mail\Mailables\Attachment[]
     */
    public function attachments()
    {
        return [
            Attachment::fromStorage('/path/to/file'),
        ];
    }

もちろん、添付ファイルの名前と MIME タイプを指定することもできます。

    /**
     * Get the attachments for the message.
     *
     * @return \Illuminate\Mail\Mailables\Attachment[]
     */
    public function attachments()
    {
        return [
            Attachment::fromStorage('/path/to/file')
                    ->as('name.pdf')
                    ->withMime('application/pdf'),
        ];
    }

デフォルトのディスク以外のストレージ ディスクを指定する必要がある場合は、`fromStorageDisk` メソッドを使用できます。

    /**
     * Get the attachments for the message.
     *
     * @return \Illuminate\Mail\Mailables\Attachment[]
     */
    public function attachments()
    {
        return [
            Attachment::fromStorageDisk('s3', '/path/to/file')
                    ->as('name.pdf')
                    ->withMime('application/pdf'),
        ];
    }

<a name="raw-data-attachments"></a>
#### 生データの添付ファイル

`fromData` 添付メソッドを使用して、生のバイト文字列を添付ファイルとして添付できます。たとえば、メモリ内に PDF を生成し、それをディスクに書き込まずに電子メールに添付したい場合は、この方法を使用できます。 `fromData` メソッドは、生データ バイトと添付ファイルに割り当てる名前を解決するクロージャを受け入れます。

    /**
     * Get the attachments for the message.
     *
     * @return \Illuminate\Mail\Mailables\Attachment[]
     */
    public function attachments()
    {
        return [
            Attachment::fromData(fn () => $this->pdf, 'Report.pdf')
                    ->withMime('application/pdf'),
        ];
    }

<a name="inline-attachments"></a>
### インライン添付ファイル

通常、電子メールにインライン画像を埋め込むのは面倒です。ただし、Laravel では、メールに画像を添付する便利な方法が提供されています。インライン画像を埋め込むには、電子メール テンプレート内の `$message` 変数で `embed` メソッドを使用します。 Laravel は自動的に `$message` 変数をすべての電子メール テンプレートで利用できるようにするため、手動で渡すことを心配する必要はありません。

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> **警告**
> プレーン テキスト メッセージはインライン添付ファイルを利用しないため、`$message` 変数はプレーン テキスト メッセージ テンプレートでは使用できません。

<a name="embedding-raw-data-attachments"></a>
#### 生データの添付ファイルの埋め込み

電子メール テンプレートに埋め込みたい生の画像データ文字列が既にある場合は、`$message` 変数で `embedData` メソッドを呼び出すことができます。 `embedData` メソッドを呼び出すときは、埋め込み画像に割り当てるファイル名を指定する必要があります。

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### 取り付け可能なオブジェクト

多くの場合、単純な文字列パスを介してメッセージにファイルを添付するだけで十分ですが、多くの場合、アプリケーション内の添付可能なエンティティはクラスによって表されます。たとえば、アプリケーションがメッセージに写真を添付し​​ている場合、アプリケーションにはその写真を表す `Photo` モデルも含まれる可能性があります。その場合、`Photo` モデルを `attach` メソッドに渡すだけで便利ではないでしょうか。アタッチ可能なオブジェクトを使用すると、まさにそれが可能になります。

まず、メッセージに添付できるオブジェクトに `Illuminate\Contracts\Mail\Attachable` インターフェイスを実装します。このインターフェイスは、クラスが `Illuminate\Mail\Attachment` インスタンスを返す `toMailAttachment` メソッドを定義することを指示します。

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Mail\Attachable;
    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Mail\Attachment;

    class Photo extends Model implements Attachable
    {
        /**
         * Get the attachable representation of the model.
         *
         * @return \Illuminate\Mail\Attachment
         */
        public function toMailAttachment()
        {
            return Attachment::fromPath('/path/to/file');
        }
    }

添付可能なオブジェクトを定義したら、電子メール メッセージを作成するときに `attachments` メソッドからそのオブジェクトのインスタンスを返すことができます。

    /**
     * Get the attachments for the message.
     *
     * @return array
     */
    public function attachments()
    {
        return [$this->photo];
    }

もちろん、添付データは Amazon S3 などのリモート ファイルストレージ サービスに保存される場合があります。したがって、Laravel では、アプリケーションの [ファイルシステムディスク](/docs/{{version}}/filesystem) の 1 つに保存されているデータから添付ファイル インスタンスを生成することもできます。

    // Create an attachment from a file on your default disk...
    return Attachment::fromStorage($this->path);

    // Create an attachment from a file on a specific disk...
    return Attachment::fromStorageDisk('backblaze', $this->path);

さらに、メモリ内にあるデータを使用して添付ファイルのインスタンスを作成することもできます。これを実現するには、`fromData` メソッドにクロージャーを提供します。クロージャは添付ファイルを表す生データを返す必要があります。

    return Attachment::fromData(fn () => $this->content, 'Photo Name');

Laravel は、添付ファイルをカスタマイズするために使用できる追加のメソッドも提供します。たとえば、`as` メソッドと `withMime` メソッドを使用して、ファイル名と MIME タイプをカスタマイズできます。

    return Attachment::fromPath('/path/to/file')
            ->as('Photo Name')
            ->withMime('image/jpeg');

<a name="headers"></a>
### ヘッダー

場合によっては、送信メッセージに追加のヘッダーを添付する必要がある場合があります。たとえば、カスタム `Message-Id` またはその他の任意のテキスト ヘッダーを設定する必要がある場合があります。

これを実現するには、メール可能ファイルで `headers` メソッドを定義します。 `headers` メソッドは、`Illuminate\Mail\Mailables\Headers` インスタンスを返す必要があります。このクラスは、`messageId`、`references`、および `text` パラメーターを受け入れます。もちろん、特定のメッセージに必要なパラメータのみを指定することもできます。

    use Illuminate\Mail\Mailables\Headers;

    /**
     * Get the message headers.
     *
     * @return \Illuminate\Mail\Mailables\Headers
     */
    public function headers()
    {
        return new Headers(
            messageId: 'custom-message-id@example.com',
            references: ['previous-message@example.com'],
            text: [
                'X-Custom-Header' => 'Custom Value',
            ],
        );
    }

<a name="tags-and-metadata"></a>
### タグとメタデータ

Mailgun や Postmark などの一部のサードパーティ電子メール プロバイダは、メッセージの「タグ」と「メタデータ」をサポートしています。これらは、アプリケーションによって送信された電子メールをグループ化し、追跡するために使用される場合があります。 `Envelope` 定義を使用して、電子メール メッセージにタグとメタデータを追加できます。

    use Illuminate\Mail\Mailables\Envelope;

    /**
     * Get the message envelope.
     *
     * @return \Illuminate\Mail\Mailables\Envelope
     */
    public function envelope()
    {
        return new Envelope(
            subject: 'Order Shipped',
            tags: ['shipment'],
            metadata: [
                'order_id' => $this->order->id,
            ],
        );
    }

アプリケーションが Mailgun ドライバを使用している場合、[tags](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1) および [metadata](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages) の詳細については、Mailgun のドキュメントを参照してください。同様に、[tags](https://postmarkapp.com/blog/tags-support-for-smtp) および [metadata](https://postmarkapp.com/support/article/1125-custom-metadata-faq) のサポートの詳細については、消印のドキュメントを参照することもできます。

アプリケーションが Amazon SES を使用して E メールを送信している場合は、`metadata` メソッドを使用してメッセージに [SESの「タグ」](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html) を添付する必要があります。

<a name="customizing-the-symfony-message"></a>
### Symfony メッセージのカスタマイズ

Laravel のメール機能は Symfony Mailer によって強化されています。 Laravel では、メッセージを送信する前に Symfony Message インスタンスで呼び出されるカスタム コールバックを登録できます。これにより、メッセージを送信する前にメッセージを詳細にカスタマイズする機会が得られます。これを実現するには、`Envelope` 定義で `using` パラメータを定義します。

    use Illuminate\Mail\Mailables\Envelope;
    use Symfony\Component\Mime\Email;
    
    /**
     * Get the message envelope.
     *
     * @return \Illuminate\Mail\Mailables\Envelope
     */
    public function envelope()
    {
        return new Envelope(
            subject: 'Order Shipped',
            using: [
                function (Email $message) {
                    // ...
                },
            ]
        );
    }

<a name="markdown-mailables"></a>
## マークダウン メール可能ファイル (Markdown Mailables)

マークダウンのメール可能メッセージを使用すると、メール可能メッセージで事前に構築されたテンプレートと [メール通知](/docs/{{version}}/notifications#mail-notifications) のコンポーネントを利用できます。メッセージは Markdown で記述されているため、Laravel はメッセージ用の美しく応答性の高い HTML テンプレートをレンダリングできると同時に、対応するプレーンテキストも自動的に生成します。

<a name="generating-markdown-mailables"></a>
### マークダウン メール可能ファイルの生成

対応する Markdown テンプレートを使用してメール可能ファイルを生成するには、`make:mail` Artisan コマンドの `--markdown` オプションを使用できます。

```shell
php artisan make:mail OrderShipped --markdown=emails.orders.shipped
```

次に、`content` メソッド内でメール可能な `Content` 定義を構成するときに、`view` パラメーターの代わりに `markdown` パラメーターを使用します。

    use Illuminate\Mail\Mailables\Content;

    /**
     * Get the message content definition.
     *
     * @return \Illuminate\Mail\Mailables\Content
     */
    public function content()
    {
        return new Content(
            markdown: 'emails.orders.shipped',
            with: [
                'url' => $this->orderUrl,
            ],
        );
    }

<a name="writing-markdown-messages"></a>
### マークダウンメッセージの作成

Markdown メール可能ファイルは、Blade コンポーネントと Markdown 構文の組み合わせを使用するため、Laravel の事前構築済み電子メール UI コンポーネントを活用しながら、メール メッセージを簡単に作成できます。

```blade
<x-mail::message>
# Order Shipped

Your order has been shipped!

<x-mail::button :url="$url">
View Order
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```

> **注記**
> Markdown メールを作成するときは、過剰なインデントを使用しないでください。 Markdown 標準に従って、Markdown パーサーはインデントされたコンテンツをコード ブロックとしてレンダリングします。

<a name="button-component"></a>
#### ボタンコンポーネント

ボタン コンポーネントは、中央にボタン リンクをレンダリングします。このコンポーネントは、`url` とオプションの `color` の 2 つの引数を受け入れます。サポートされている色は、`primary`、`success`、および `error` です。ボタン コンポーネントは必要なだけメッセージに追加できます。

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### パネルコンポーネント

パネル コンポーネントは、メッセージの残りの部分とはわずかに異なる背景色を持つパネルに指定されたテキスト ブロックをレンダリングします。これにより、特定のテキスト ブロックに注意を向けることができます。

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### テーブルコンポーネント

table コンポーネントを使用すると、Markdown テーブルを HTML テーブルに変換できます。コンポーネントは、Markdown テーブルをコンテンツとして受け入れます。テーブル列の配置は、デフォルトの Markdown テーブル配置構文を使用してサポートされます。

```blade
<x-mail::table>
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### コンポーネントのカスタマイズ

すべての Markdown メール コンポーネントを独自のアプリケーションにエクスポートしてカスタマイズできます。コンポーネントをエクスポートするには、`vendor:publish` Artisan コマンドを使用して、`laravel-mail` アセット タグを公開します。

```shell
php artisan vendor:publish --tag=laravel-mail
```

このコマンドは、Markdown メール コンポーネントを `resources/views/vendor/mail` ディレクトリに公開します。 `mail` ディレクトリには、`html` ディレクトリと `text` ディレクトリが含まれ、それぞれに使用可能なすべてのコンポーネントのそれぞれの表現が含まれます。これらのコンポーネントは自由にカスタマイズできます。

<a name="customizing-the-css"></a>
#### CSS のカスタマイズ

コンポーネントをエクスポートすると、`resources/views/vendor/mail/html/themes` ディレクトリに `default.css` ファイルが含まれます。このファイル内の CSS をカスタマイズすると、スタイルは Markdown メール メッセージの HTML 表現内のインライン CSS スタイルに自動的に変換されます。

Laravel の Markdown コンポーネント用にまったく新しいテーマを構築したい場合は、CSS ファイルを `html/themes` ディレクトリ内に配置できます。 CSS ファイルに名前を付けて保存した後、アプリケーションの `config/mail.php` 構成ファイルの `theme` オプションを新しいテーマの名前と一致するように更新します。

個々のメール可能ファイルのテーマをカスタマイズするには、メール可能クラスの `$theme` プロパティを、そのメール可能ファイルの送信時に使用するテーマの名前に設定します。

<a name="sending-mail"></a>
## メールの送信 (Sending Mail)

メッセージを送信するには、`Mail` [facade](/docs/{{version}}/facades) で `to` メソッドを使用します。 `to` メソッドは、電子メール アドレス、ユーザー インスタンス、またはユーザーのコレクションを受け入れます。オブジェクトまたはオブジェクトのコレクションを渡す場合、メーラーは電子メールの受信者を決定するときに `email` および `name` プロパティを自動的に使用するため、これらの属性がオブジェクトで使用できることを確認してください。受信者を指定したら、メール可能クラスのインスタンスを `send` メソッドに渡すことができます。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Mail\OrderShipped;
    use App\Models\Order;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Mail;

    class OrderShipmentController extends Controller
    {
        /**
         * Ship the given order.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function store(Request $request)
        {
            $order = Order::findOrFail($request->order_id);

            // Ship the order...

            Mail::to($request->user())->send(new OrderShipped($order));
        }
    }

メッセージを送信するときは、受信者の「宛先」を指定するだけではありません。それぞれのメソッドを連鎖させることで、「to」、「cc」、「bcc」の受信者を自由に設定できます。

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->send(new OrderShipped($order));

<a name="looping-over-recipients"></a>
#### 受信者をループする

場合によっては、受信者/電子メール アドレスの配列を反復処理して、受信者のリストにメール可能ファイルを送信する必要がある場合があります。ただし、`to` メソッドは電子メール アドレスをメール可能受信者のリストに追加するため、ループを繰り返すたびに、前のすべての受信者に別の電子メールが送信されます。したがって、受信者ごとにメール可能インスタンスを常に再作成する必要があります。

    foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
        Mail::to($recipient)->send(new OrderShipped($order));
    }

<a name="sending-mail-via-a-specific-mailer"></a>
#### 特定のメーラー経由でメールを送信する

デフォルトでは、Laravel はアプリケーションの `mail` 設定ファイルで `default` メーラーとして設定されたメーラーを使用して電子メールを送信します。ただし、`mailer` メソッドを使用して、特定のメーラー構成を使用してメッセージを送信することもできます。

    Mail::mailer('postmark')
            ->to($request->user())
            ->send(new OrderShipped($order));

<a name="queueing-mail"></a>
### メールのキューイング

<a name="queueing-a-mail-message"></a>
#### メールメッセージをキューに入れる

電子メール メッセージの送信はアプリケーションの応答時間に悪影響を与える可能性があるため、多くの開発者はバックグラウンド送信のために電子メール メッセージをキューに入れることを選択します。 Laravel では、組み込みの [統合キューAPI](/docs/{{version}}/queues) を使用してこれを簡単に実行できます。メール メッセージをキューに入れるには、メッセージの受信者を指定した後、`Mail` ファサードで `queue` メソッドを使用します。

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->queue(new OrderShipped($order));

このメソッドは、ジョブをキューにプッシュする処理を自動的に処理するため、メッセージはバックグラウンドで送信されます。この機能を使用する前に、[キューを設定する](/docs/{{version}}/queues) する必要があります。

<a name="delayed-message-queueing"></a>
#### 遅延メッセージキューイング

キューに入れられた電子メール メッセージの配信を遅らせたい場合は、`later` メソッドを使用できます。 `later` メソッドは、最初の引数として、メッセージをいつ送信するかを示す `DateTime` インスタンスを受け取ります。

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->later(now()->addMinutes(10), new OrderShipped($order));

<a name="pushing-to-specific-queues"></a>
#### 特定のキューへのプッシュ

`make:mail` コマンドを使用して生成されたすべてのメール可能クラスは `Illuminate\Bus\Queueable` 特性を利用するため、任意のメール可能クラス インスタンスで `onQueue` メソッドと `onConnection` メソッドを呼び出して、メッセージの接続とキュー名を指定できます。

    $message = (new OrderShipped($order))
                    ->onConnection('sqs')
                    ->onQueue('emails');

    Mail::to($request->user())
        ->cc($moreUsers)
        ->bcc($evenMoreUsers)
        ->queue($message);

<a name="queueing-by-default"></a>
#### デフォルトでのキューイング

常にキューに入れておきたいメール可能なクラスがある場合は、そのクラスに `ShouldQueue` コントラクトを実装できます。ここで、メール送信時に `send` メソッドを呼び出したとしても、メール可能ファイルはコントラクトを実装しているため、引き続きキューに入れられます。

    use Illuminate\Contracts\Queue\ShouldQueue;

    class OrderShipped extends Mailable implements ShouldQueue
    {
        //
    }

<a name="queued-mailables-and-database-transactions"></a>
#### キューに入れられたメール可能ファイルとデータベース トランザクション

キューに入れられたメール可能ファイルがデータベース トランザクション内でディスパッチされると、データベース トランザクションがコミットされる前にキューによって処理される可能性があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに対して行った更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。メール可能ファイルがこれらのモデルに依存している場合、キューに入れられたメール可能ファイルを送信するジョブの処理時に予期しないエラーが発生する可能性があります。

キュー接続の `after_commit` 構成オプションが `false` に設定されている場合でも、メール メッセージの送信時に `afterCommit` メソッドを呼び出して、開いているすべてのデータベース トランザクションがコミットされた後に特定のキューに入れられたメール可能ファイルをディスパッチする必要があることを指定できます。

    Mail::to($request->user())->send(
        (new OrderShipped($order))->afterCommit()
    );

あるいは、メール可能ファイルのコンストラクターから `afterCommit` メソッドを呼び出すこともできます。

    <?php

    namespace App\Mail;

    use Illuminate\Bus\Queueable;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Mail\Mailable;
    use Illuminate\Queue\SerializesModels;

    class OrderShipped extends Mailable implements ShouldQueue
    {
        use Queueable, SerializesModels;

        /**
         * Create a new message instance.
         *
         * @return void
         */
        public function __construct()
        {
            $this->afterCommit();
        }
    }

> **注記**
> これらの問題の回避方法の詳細については、[キューに入れられたジョブとデータベース トランザクション](/docs/{{version}}/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="rendering-mailables"></a>
## メール可能ファイルのレンダリング (Rendering Mailables)

メール可能ファイルを送信せずに、その HTML コンテンツをキャプチャしたい場合があります。これを実現するには、メール可能ファイルの `render` メソッドを呼び出します。このメソッドは、メール可能ファイルの評価された HTML コンテンツを文字列として返します。

    use App\Mail\InvoicePaid;
    use App\Models\Invoice;

    $invoice = Invoice::find(1);

    return (new InvoicePaid($invoice))->render();

<a name="previewing-mailables-in-the-browser"></a>
### ブラウザでのメール可能ファイルのプレビュー

メール可能ファイルのテンプレートを設計する場合、一般的な Blade テンプレートと同様に、レンダリングされたメール可能ファイルをブラウザーですばやくプレビューできると便利です。このため、Laravel では、ルート クロージャーまたはコントローラから直接メール可能ファイルを返すことができます。メール可能ファイルが返されると、レンダリングされてブラウザに表示されるため、実際の電子メール アドレスに送信しなくても、そのデザインをすばやくプレビューできます。

    Route::get('/mailable', function () {
        $invoice = App\Models\Invoice::find(1);

        return new App\Mail\InvoicePaid($invoice);
    });

> **警告**
> メール可能ファイルがブラウザでプレビューされるとき、[インライン添付ファイル](#inline-attachments) はレンダリングされません。これらのメール可能ファイルをプレビューするには、[Mailpit](https://github.com/axllent/mailpit) や [HELO](https://usehelo.com) などの電子メール テスト アプリケーションに送信する必要があります。

<a name="localizing-mailables"></a>
## メール可能ファイルのローカライズ (Localizing Mailables)

Laravel では、リクエストの現在のロケール以外のロケールでメール可能ファイルを送信することができ、メールがキューに入れられている場合でもこのロケールを記憶します。

これを実現するために、`Mail` ファサードは、希望の言語を設定するための `locale` メソッドを提供します。アプリケーションは、メール可能テンプレートの評価中にこのロケールに変更され、評価が完了すると前のロケールに戻ります。

    Mail::to($request->user())->locale('es')->send(
        new OrderShipped($order)
    );

<a name="user-preferred-locales"></a>
### ユーザーの優先ロケール

場合によっては、アプリケーションが各ユーザーの優先ロケールを保存することがあります。 1 つ以上のモデルに `HasLocalePreference` コントラクトを実装することで、メール送信時にこの保存されたロケールを使用するように Laravel に指示できます。

    use Illuminate\Contracts\Translation\HasLocalePreference;

    class User extends Model implements HasLocalePreference
    {
        /**
         * Get the user's preferred locale.
         *
         * @return string
         */
        public function preferredLocale()
        {
            return $this->locale;
        }
    }

インターフェースを実装すると、Laravel はメール可能ファイルや通知をモデルに送信するときに優先ロケールを自動的に使用します。したがって、このインターフェイスを使用する場合は、`locale` メソッドを呼び出す必要はありません。

    Mail::to($request->user())->send(new OrderShipped($order));

<a name="testing-mailables"></a>
## メール可能ファイルのテスト (Testing Mailables)

Laravel は、メーラブルの構造を検査するためのさまざまな方法を提供します。さらに、Laravel には、メール可能ファイルに期待するコンテンツが含まれているかどうかをテストするための便利な方法がいくつか用意されています。これらのメソッドは、`assertSeeInHtml`、`assertDontSeeInHtml`、`assertSeeInOrderInHtml`、`assertSeeInText`、`assertDontSeeInText`、`assertSeeInOrderInText`、`assertHasAttachment`、`assertHasAttachedData`、`assertHasAttachmentFromStorage`、および `assertHasAttachmentFromStorageDisk` です。

ご想像のとおり、「HTML」アサーションはメール可能ファイルの HTML バージョンに指定された文字列が含まれることをアサートし、「テキスト」アサーションはメール可能ファイルのプレーンテキスト バージョンに指定された文字列が含まれることをアサートします。

    use App\Mail\InvoicePaid;
    use App\Models\User;

    public function test_mailable_content()
    {
        $user = User::factory()->create();

        $mailable = new InvoicePaid($user);

        $mailable->assertFrom('jeffrey@example.com');
        $mailable->assertTo('taylor@example.com');
        $mailable->assertHasCc('abigail@example.com');
        $mailable->assertHasBcc('victoria@example.com');
        $mailable->assertHasReplyTo('tyler@example.com');
        $mailable->assertHasSubject('Invoice Paid');
        $mailable->assertHasTag('example-tag');
        $mailable->assertHasMetadata('key', 'value');

        $mailable->assertSeeInHtml($user->email);
        $mailable->assertSeeInHtml('Invoice Paid');
        $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

        $mailable->assertSeeInText($user->email);
        $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

        $mailable->assertHasAttachment('/path/to/file');
        $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
        $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
        $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
        $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    }

<a name="testing-mailable-sending"></a>
#### メール可能な送信のテスト

特定のメール可能ファイルが特定のユーザーに「送信された」ことを確認するテストとは別に、メール可能ファイルのコンテンツをテストすることをお勧めします。メール可能ファイルが送信されたことをテストする方法については、[偽メール](/docs/{{version}}/mocking#mail-fake) のドキュメントを参照してください。

<a name="mail-and-local-development"></a>
## メールとローカル開発 (Mail & Local Development)

電子メールを送信するアプリケーションを開発する場合、実際には実際の電子メール アドレスに電子メールを送信したくないでしょう。 Laravel には、ローカル開発中に実際の電子メールの送信を「無効にする」方法がいくつか用意されています。

<a name="log-driver"></a>
#### ログドライバ

電子メールを送信する代わりに、`log` メール ドライバは検査のためにすべての電子メール メッセージをログ ファイルに書き込みます。通常、このドライバはローカル開発中にのみ使用されます。環境ごとのアプリケーションの構成の詳細については、[設定ドキュメント](/docs/{{version}}/configuration#environment-configuration) を確認してください。

<a name="mailtrap"></a>
#### HELO / メールトラップ / メールピット

あるいは、[HELO](https://usehelo.com) や [Mailtrap](https://mailtrap.io) などのサービスと `smtp` ドライバを使用して、電子メール メッセージを「ダミー」メールボックスに送信し、実際の電子メール クライアントで表示することもできます。このアプローチには、Mailtrap のメッセージ ビューアで最終的な電子メールを実際に検査できるという利点があります。

[Laravel Sail](/docs/{{version}}/sail) を使用している場合は、[Mailpit](https://github.com/axllent/mailpit) を使用してメッセージをプレビューできます。 Sail の実行中は、`http://localhost:8025` で Mailpit インターフェイスにアクセスできます。

<a name="using-a-global-to-address"></a>
#### グローバル `to` アドレスの使用

最後に、`Mail` ファサードが提供する `alwaysTo` メソッドを呼び出して、グローバル "to" アドレスを指定できます。通常、このメソッドは、アプリケーションのサービスプロバイダの 1 つの `boot` メソッドから呼び出す必要があります。

    use Illuminate\Support\Facades\Mail;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        if ($this->app->environment('local')) {
            Mail::alwaysTo('taylor@example.com');
        }
    }

<a name="events"></a>
## イベント (Events)

Laravel は、メールメッセージの送信プロセス中に 2 つのイベントを発生させます。 `MessageSending` イベントはメッセージの送信前に発生しますが、`MessageSent` イベントはメッセージの送信後に発生します。これらのイベントは、メールがキューに入れられたときではなく、*送信*されたときに発生することに注意してください。 `App\Providers\EventServiceProvider` サービスプロバイダでこのイベントのイベント リスナを登録できます。

    use App\Listeners\LogSendingMessage;
    use App\Listeners\LogSentMessage;
    use Illuminate\Mail\Events\MessageSending;
    use Illuminate\Mail\Events\MessageSent;
    
    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        MessageSending::class => [
            LogSendingMessage::class,
        ],

        MessageSent::class => [
            LogSentMessage::class,
        ],
    ];

<a name="custom-transports"></a>
## カスタムトランスポート (Custom Transports)

Laravel にはさまざまなメールトランスポートが含まれています。ただし、Laravel がそのままではサポートしていない他のサービスを介して電子メールを配信するために、独自のトランスポートを作成することもできます。まず、`Symfony\Component\Mailer\Transport\AbstractTransport` クラスを拡張するクラスを定義します。次に、トランスポートに `doSend` メソッドと `__toString()` メソッドを実装します。

    use MailchimpTransactional\ApiClient;
    use Symfony\Component\Mailer\SentMessage;
    use Symfony\Component\Mailer\Transport\AbstractTransport;
    use Symfony\Component\Mime\MessageConverter;

    class MailchimpTransport extends AbstractTransport
    {
        /**
         * The Mailchimp API client.
         *
         * @var \MailchimpTransactional\ApiClient
         */
        protected $client;

        /**
         * Create a new Mailchimp transport instance.
         *
         * @param  \MailchimpTransactional\ApiClient  $client
         * @return void
         */
        public function __construct(ApiClient $client)
        {
            parent::__construct();
            
            $this->client = $client;
        }

        /**
         * {@inheritDoc}
         */
        protected function doSend(SentMessage $message): void
        {
            $email = MessageConverter::toEmail($message->getOriginalMessage());

            $this->client->messages->send(['message' => [
                'from_email' => $email->getFrom(),
                'to' => collect($email->getTo())->map(function ($email) {
                    return ['email' => $email->getAddress(), 'type' => 'to'];
                })->all(),
                'subject' => $email->getSubject(),
                'text' => $email->getTextBody(),
            ]]);
        }

        /**
         * Get the string representation of the transport.
         *
         * @return string
         */
        public function __toString(): string
        {
            return 'mailchimp';
        }
    }

カスタム トランスポートを定義したら、`Mail` ファサードによって提供される `extend` メソッドを介して登録できます。通常、これはアプリケーションの `AppServiceProvider` サービスプロバイダの `boot` メソッド内で実行する必要があります。 `$config` 引数は、`extend` メソッドに提供されたクロージャに渡されます。この引数には、アプリケーションの `config/mail.php` 構成ファイルでメーラーに対して定義された構成配列が含まれます。

    use App\Mail\MailchimpTransport;
    use Illuminate\Support\Facades\Mail;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Mail::extend('mailchimp', function (array $config = []) {
            return new MailchimpTransport(/* ... */);
        });
    }

カスタム トランスポートを定義して登録したら、新しいトランスポートを利用するアプリケーションの `config/mail.php` 構成ファイル内にメーラー定義を作成できます。

    'mailchimp' => [
        'transport' => 'mailchimp',
        // ...
    ],

<a name="additional-symfony-transports"></a>
### 追加の Symfony トランスポート

Laravel には、Mailgun や Postmark など、Symfony が管理する既存のメールトランスポートのサポートが含まれています。ただし、追加の Symfony 管理トランスポートをサポートして Laravel を拡張したい場合もあります。これを行うには、Composer 経由で必要な Symfony Mailerを要求し、トランスポートを Laravel に登録します。たとえば、「Sendinblue」Symfony Mailerをインストールして登録できます。

```none
composer require symfony/sendinblue-mailer symfony/http-client
```

Sendinblue メーラー パッケージがインストールされたら、Sendinblue API 資格情報のエントリをアプリケーションの `services` 構成ファイルに追加できます。

    'sendinblue' => [
        'key' => 'your-api-key',
    ],

次に、`Mail` ファサードの `extend` メソッドを使用して、トランスポートを Laravel に登録できます。通常、これはサービスプロバイダの `boot` メソッド内で実行する必要があります。

    use Illuminate\Support\Facades\Mail;
    use Symfony\Component\Mailer\Bridge\Sendinblue\Transport\SendinblueTransportFactory;
    use Symfony\Component\Mailer\Transport\Dsn;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Mail::extend('sendinblue', function () {
            return (new SendinblueTransportFactory)->create(
                new Dsn(
                    'sendinblue+api',
                    'default',
                    config('services.sendinblue.key')
                )
            );
        });
    }

トランスポートが登録されたら、アプリケーションの config/mail.php 設定ファイル内に新しいトランスポートを利用するメーラー定義を作成できます。

    'sendinblue' => [
        'transport' => 'sendinblue',
        // ...
    ],


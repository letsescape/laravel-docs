<!-- # Mail -->
# Mail

- [Introduction](#introduction)
    - [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
    - [Failover Configuration](#failover-configuration)
- [Generating Mailables](#generating-mailables)
- [Writing Mailables](#writing-mailables)
    - [Configuring The Sender](#configuring-the-sender)
    - [Configuring The View](#configuring-the-view)
    - [View Data](#view-data)
    - [Attachments](#attachments)
    - [Inline Attachments](#inline-attachments)
    - [Customizing The SwiftMailer Message](#customizing-the-swiftmailer-message)
- [Markdown Mailables](#markdown-mailables)
    - [Generating Markdown Mailables](#generating-markdown-mailables)
    - [Writing Markdown Messages](#writing-markdown-messages)
    - [Customizing The Components](#customizing-the-components)
- [Sending Mail](#sending-mail)
    - [Queueing Mail](#queueing-mail)
- [Rendering Mailables](#rendering-mailables)
    - [Previewing Mailables In The Browser](#previewing-mailables-in-the-browser)
- [Localizing Mailables](#localizing-mailables)
- [Testing Mailables](#testing-mailables)
- [Mail & Local Development](#mail-and-local-development)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Sending email doesn't have to be complicated. Laravel provides a clean, simple email API powered by the popular [SwiftMailer](https://swiftmailer.symfony.com/) library. Laravel and SwiftMailer provide drivers for sending email via SMTP, Mailgun, Postmark, Amazon SES, and `sendmail`, allowing you to quickly get started sending mail through a local or cloud based service of your choice. -->
電子メールの送信は複雑である必要はありません。 Laravel は、人気のある [SwiftMailer](https://swiftmailer.symfony.com/) ライブラリを活用したクリーンでシンプルな電子メール API を提供します。 Laravel と SwiftMailer は、SMTP、Mailgun、Postmark、Amazon SES、および `sendmail` 経由で電子メールを送信するためのドライバを提供しており、選択したローカルまたはクラウドベースのサービスを通じてメールの送信をすぐに開始できます。

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Laravel's email services may be configured via your application's `config/mail.php` configuration file. Each mailer configured within this file may have its own unique configuration and even its own unique "transport", allowing your application to use different email services to send certain email messages. For example, your application might use Postmark to send transactional emails while using Amazon SES to send bulk emails. -->
Laravel の電子メール サービスは、アプリケーションの `config/mail.php` 構成ファイルを介して構成できます。このファイル内で構成された各メーラーは、独自の固有の構成および独自の「トランスポート」さえ持つことができ、アプリケーションがさまざまな電子メール サービスを使用して特定の電子メール メッセージを送信できるようになります。たとえば、アプリケーションでは Postmark を使用してトランザクション E メールを送信し、Amazon SES を使用して一括 E メールを送信する場合があります。

<!-- Within your `mail` configuration file, you will find a `mailers` configuration array. This array contains a sample configuration entry for each of the major mail drivers / transports supported by Laravel, while the `default` configuration value determines which mailer will be used by default when your application needs to send an email message. -->
`mail` 構成ファイル内に、`mailers` 構成配列があります。この配列には、Laravel でサポートされている主要なメールドライバ/トランスポートのそれぞれのサンプル構成エントリが含まれています。一方、`default` 構成値は、アプリケーションが電子メールメッセージを送信する必要があるときにデフォルトで使用されるメーラーを決定します。

<a name="driver-prerequisites"></a>
<!-- ### Driver / Transport Prerequisites -->
### Driver / Transport Prerequisites

<!-- The API based drivers such as Mailgun and Postmark are often simpler and faster than sending mail via SMTP servers. Whenever possible, we recommend that you use one of these drivers. All of the API based drivers require the Guzzle HTTP library, which may be installed via the Composer package manager: -->
Mailgun や Postmark などの API ベースのドライバは、多くの場合、SMTP サーバー経由でメールを送信するよりも簡単で高速です。可能な限り、これらのドライバのいずれかを使用することをお勧めします。すべての API ベースのドライバには Guzzle HTTP ライブラリが必要です。これは Composer パッケージ マネージャー経由でインストールできます。

```
composer require guzzlehttp/guzzle
```

<a name="mailgun-driver"></a>
<!-- #### Mailgun Driver -->
#### Mailgun Driver

<!-- To use the Mailgun driver, first install the Guzzle HTTP library. Then, set the `default` option in your `config/mail.php` configuration file to `mailgun`. Next, verify that your `config/services.php` configuration file contains the following options: -->
Mailgun ドライバを使用するには、まず Guzzle HTTP ライブラリをインストールします。次に、`config/mail.php` 構成ファイルの `default` オプションを `mailgun` に設定します。次に、`config/services.php` 構成ファイルに次のオプションが含まれていることを確認します。

```
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
],
```

<!-- If you are not using the United States [Mailgun region](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions), you may define your region's endpoint in the `services` configuration file: -->
米国の [Mailgun region](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions) を使用していない場合は、`services` 構成ファイルで地域のエンドポイントを定義できます。

```
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
],
```

<a name="postmark-driver"></a>
<!-- #### Postmark Driver -->
#### Postmark Driver

<!-- To use the Postmark driver, install Postmark's SwiftMailer transport via Composer: -->
Postmark ドライバを使用するには、Composer 経由で Postmark の SwiftMailer トランスポートをインストールします。

```
composer require wildbit/swiftmailer-postmark
```

<!-- Next, install the Guzzle HTTP library and set the `default` option in your `config/mail.php` configuration file to `postmark`. Finally, verify that your `config/services.php` configuration file contains the following options: -->
次に、Guzzle HTTP ライブラリをインストールし、`config/mail.php` 構成ファイルの `default` オプションを `postmark` に設定します。最後に、`config/services.php` 構成ファイルに次のオプションが含まれていることを確認します。

```
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

<!-- If you would like to specify the Postmark message stream that should be used by a given mailer, you may add the `message_stream_id` configuration option to the mailer's configuration array. This configuration array can be found in your application's `config/mail.php` configuration file: -->
特定のメーラーで使用する Postmark メッセージ ストリームを指定したい場合は、メーラーの構成配列に `message_stream_id` 構成オプションを追加できます。この構成配列は、アプリケーションの `config/mail.php` 構成ファイルにあります。

```
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
],
```

<!-- This way you are also able to set up multiple Postmark mailers with different message streams. -->
この方法では、異なるメッセージ ストリームを持つ複数の Postmark メーラーを設定することもできます。

<a name="ses-driver"></a>
<!-- #### SES Driver -->
#### SES Driver

<!-- To use the Amazon SES driver you must first install the Amazon AWS SDK for PHP. You may install this library via the Composer package manager: -->
Amazon SES ドライバを使用するには、まず Amazon AWS SDK for PHP をインストールする必要があります。このライブラリは、Composer パッケージ マネージャーを介してインストールできます。

```bash
composer require aws/aws-sdk-php
```

<!-- Next, set the `default` option in your `config/mail.php` configuration file to `ses` and verify that your `config/services.php` configuration file contains the following options: -->
次に、`config/mail.php` 構成ファイルの `default` オプションを `ses` に設定し、`config/services.php` 構成ファイルに次のオプションが含まれていることを確認します。

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

<!-- To utilize AWS [temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html) via a session token, you may add a `token` key to your application's SES configuration: -->
セッション トークン経由で AWS [temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html) を利用するには、アプリケーションの SES 設定に `token` キーを追加します。

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

<!-- If you would like to define [additional options](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-email-2010-12-01.html#sendrawemail) that Laravel should pass to the AWS SDK's `SendRawEmail` method when sending an email, you may define an `options` array within your `ses` configuration: -->
電子メールの送信時に Laravel が AWS SDK の `SendRawEmail` メソッドに渡す [additional options](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-email-2010-12-01.html#sendrawemail) を定義したい場合は、`ses` 設定内で `options` 配列を定義できます。

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'options' => [
        'ConfigurationSetName' => 'MyConfigurationSet',
        'Tags' => [
            ['Name' => 'foo', 'Value' => 'bar'],
        ],
    ],
],
```

<a name="failover-configuration"></a>
<!-- ### Failover Configuration -->
### Failover Configuration

<!-- Sometimes, an external service you have configured to send your application's mail may be down. In these cases, it can be useful to define one or more backup mail delivery configurations that will be used in case your primary delivery driver is down. -->
場合によっては、アプリケーションのメールを送信するように構成した外部サービスがダウンしている可能性があります。このような場合、プライマリ配信ドライバがダウンした場合に使用されるバックアップ メール配信構成を 1 つ以上定義すると便利です。

<!-- To accomplish this, you should define a mailer within your application's `mail` configuration file that uses the `failover` transport. The configuration array for your application's `failover` mailer should contain an array of `mailers` that reference the order in which mail drivers should be chosen for delivery: -->
これを実現するには、アプリケーションの `mail` 構成ファイル内で、`failover` トランスポートを使用するメーラーを定義する必要があります。アプリケーションの `failover` メーラーの構成配列には、配信用にメール ドライバを選択する順序を参照する `mailers` の配列が含まれている必要があります。

```
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
```

<!-- Once your failover mailer has been defined, you should set this mailer as the default mailer used by your application by specifying its name as the value of the `default` configuration key within your application's `mail` configuration file: -->
フェイルオーバー メーラーを定義したら、アプリケーションの `mail` 構成ファイル内の `default` 構成キーの値としてその名前を指定することにより、このメーラーをアプリケーションで使用されるデフォルトのメーラーとして設定する必要があります。

```
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="generating-mailables"></a>
<!-- ## Generating Mailables -->
## Generating Mailables

<!-- When building Laravel applications, each type of email sent by your application is represented as a "mailable" class. These classes are stored in the `app/Mail` directory. Don't worry if you don't see this directory in your application, since it will be generated for you when you create your first mailable class using the `make:mail` Artisan command: -->
Laravel アプリケーションを構築する場合、アプリケーションによって送信される各種類の電子メールは、「メール可能」クラスとして表されます。これらのクラスは、`app/Mail` ディレクトリに保存されます。アプリケーションにこのディレクトリが表示されなくても心配する必要はありません。このディレクトリは、`make:mail` Artisan コマンドを使用して最初のメール可能クラスを作成するときに生成されるためです。

```
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
<!-- ## Writing Mailables -->
## Writing Mailables

<!-- Once you have generated a mailable class, open it up so we can explore its contents. First, note that all of a mailable class' configuration is done in the `build` method. Within this method, you may call various methods such as `from`, `subject`, `view`, and `attach` to configure the email's presentation and delivery. -->
メール可能なクラスを生成したら、そのクラスを開いて、その内容を探索できるようにします。まず、メール可能クラスの設定はすべて `build` メソッドで行われることに注意してください。このメソッド内で、`from`、`subject`、`view`、`attach` などのさまざまなメソッドを呼び出して、電子メールのプレゼンテーションと配信を構成できます。

> [!TIP]
> メール可能ファイルの `build` メソッドに対する依存関係をタイプヒントで指定できます。 Laravel [service container](/docs/8.x/container) はこれらの依存関係を自動的に挿入します。

<a name="configuring-the-sender"></a>
<!-- ### Configuring The Sender -->
### Configuring The Sender

<a name="using-the-from-method"></a>
<!-- #### Using The `from` Method -->
#### Using The `from` Method

<!-- First, let's explore configuring the sender of the email. Or, in other words, who the email is going to be "from". There are two ways to configure the sender. First, you may use the `from` method within your mailable class' `build` method: -->
まず、電子メールの送信者の構成を見てみましょう。言い換えれば、電子メールの「送信者」が誰になるのかということです。送信者を構成するには 2 つの方法があります。まず、メール可能クラスの `build` メソッド内で `from` メソッドを使用できます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
    return $this->from('example@example.com', 'Example')
                ->view('emails.orders.shipped');
}
```

<a name="using-a-global-from-address"></a>
<!-- #### Using A Global `from` Address -->
#### Using A Global `from` Address

<!-- However, if your application uses the same "from" address for all of its emails, it can become cumbersome to call the `from` method in each mailable class you generate. Instead, you may specify a global "from" address in your `config/mail.php` configuration file. This address will be used if no other "from" address is specified within the mailable class: -->
ただし、アプリケーションがすべての電子メールに同じ「差出人」アドレスを使用する場合、生成する各メール可能クラスで `from` メソッドを呼び出すのが面倒になる可能性があります。代わりに、`config/mail.php` 構成ファイルでグローバル「送信元」アドレスを指定できます。このアドレスは、メール可能クラス内に他の「差出人」アドレスが指定されていない場合に使用されます。

```
'from' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<!-- In addition, you may define a global "reply_to" address within your `config/mail.php` configuration file: -->
さらに、`config/mail.php` 構成ファイル内でグローバル「reply_to」アドレスを定義できます。

```
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
<!-- ### Configuring The View -->
### Configuring The View

<!-- Within a mailable class' `build` method, you may use the `view` method to specify which template should be used when rendering the email's contents. Since each email typically uses a [Blade template](/docs/8.x/blade) to render its contents, you have the full power and convenience of the Blade templating engine when building your email's HTML: -->
メール可能クラスの `build` メソッド内で、`view` メソッドを使用して、電子メールのコンテンツをレンダリングするときに使用するテンプレートを指定できます。通常、各電子メールは [Blade template](/docs/8.x/blade) を使用してコンテンツをレンダリングするため、電子メールの HTML を構築するときに、Blade テンプレート エンジンの能力と利便性を最大限に活用できます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
    return $this->view('emails.orders.shipped');
}
```

> [!TIP]
> すべての電子メール テンプレートを格納する `resources/views/emails` ディレクトリを作成するとよいでしょう。ただし、`resources/views` ディレクトリ内のどこにでも自由に配置できます。

<a name="plain-text-emails"></a>
<!-- #### Plain Text Emails -->
#### Plain Text Emails

<!-- If you would like to define a plain-text version of your email, you may use the `text` method. Like the `view` method, the `text` method accepts a template name which will be used to render the contents of the email. You are free to define both an HTML and plain-text version of your message: -->
電子メールのプレーンテキスト バージョンを定義したい場合は、`text` メソッドを使用できます。 `view` メソッドと同様に、`text` メソッドは、電子メールのコンテンツをレンダリングするために使用されるテンプレート名を受け入れます。メッセージの HTML バージョンとプレーンテキスト バージョンの両方を自由に定義できます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
    return $this->view('emails.orders.shipped')
                ->text('emails.orders.shipped_plain');
}
```

<a name="view-data"></a>
<!-- ### View Data -->
### View Data

<a name="via-public-properties"></a>
<!-- #### Via Public Properties -->
#### Via Public Properties

<!-- Typically, you will want to pass some data to your view that you can utilize when rendering the email's HTML. There are two ways you may make data available to your view. First, any public property defined on your mailable class will automatically be made available to the view. So, for example, you may pass data into your mailable class' constructor and set that data to public properties defined on the class: -->
通常、電子メールの HTML をレンダリングするときに利用できるデータをビューに渡す必要があります。ビューでデータを利用できるようにするには 2 つの方法があります。まず、メール可能クラスで定義されたパブリック プロパティは自動的にビューで利用できるようになります。したがって、たとえば、メール可能クラスのコンストラクターにデータを渡し、そのデータをクラスで定義されたパブリック プロパティに設定できます。

```
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
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
     * Build the message.
     *
     * @return $this
     */
    public function build()
    {
        return $this->view('emails.orders.shipped');
    }
}
```

<!-- Once the data has been set to a public property, it will automatically be available in your view, so you may access it like you would access any other data in your Blade templates: -->
データがパブリック プロパティに設定されると、そのデータは自動的にビューで使用できるようになり、Blade テンプレート内の他のデータにアクセスするのと同じようにアクセスできます。

```
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-method"></a>
<!-- #### Via The `with` Method: -->
#### Via The `with` Method:

<!-- If you would like to customize the format of your email's data before it is sent to the template, you may manually pass your data to the view via the `with` method. Typically, you will still pass data via the mailable class' constructor; however, you should set this data to `protected` or `private` properties so the data is not automatically made available to the template. Then, when calling the `with` method, pass an array of data that you wish to make available to the template: -->
電子メールのデータをテンプレートに送信する前にその形式をカスタマイズしたい場合は、`with` メソッドを使用してデータをビューに手動で渡すことができます。通常は、メール可能クラスのコンストラクターを介してデータを渡します。ただし、データがテンプレートで自動的に使用可能にならないように、このデータを `protected` または `private` プロパティに設定する必要があります。次に、`with` メソッドを呼び出すときに、テンプレートで使用できるようにするデータの配列を渡します。

```
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
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
     * Build the message.
     *
     * @return $this
     */
    public function build()
    {
        return $this->view('emails.orders.shipped')
                    ->with([
                        'orderName' => $this->order->name,
                        'orderPrice' => $this->order->price,
                    ]);
    }
}
```

<!-- Once the data has been passed to the `with` method, it will automatically be available in your view, so you may access it like you would access any other data in your Blade templates: -->
データが `with` メソッドに渡されると、そのデータはビューで自動的に使用可能になるため、Blade テンプレート内の他のデータにアクセスするのと同じようにアクセスできます。

```
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
<!-- ### Attachments -->
### Attachments

<!-- To add attachments to an email, use the `attach` method within the mailable class' `build` method. The `attach` method accepts the full path to the file as its first argument: -->
電子メールに添付ファイルを追加するには、メール可能クラスの `build` メソッド内で `attach` メソッドを使用します。 `attach` メソッドは、ファイルへのフルパスを最初の引数として受け入れます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
    return $this->view('emails.orders.shipped')
                ->attach('/path/to/file');
}
```

<!-- When attaching files to a message, you may also specify the display name and / or MIME type by passing an `array` as the second argument to the `attach` method: -->
メッセージにファイルを添付するときは、`array` を `attach` メソッドの 2 番目の引数として渡すことで、表示名や MIME タイプを指定することもできます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
    return $this->view('emails.orders.shipped')
                ->attach('/path/to/file', [
                    'as' => 'name.pdf',
                    'mime' => 'application/pdf',
                ]);
}
```

<a name="attaching-files-from-disk"></a>
<!-- #### Attaching Files From Disk -->
#### Attaching Files From Disk

<!-- If you have stored a file on one of your [filesystem disks](/docs/8.x/filesystem), you may attach it to the email using the `attachFromStorage` method: -->
[filesystem disks](/docs/8.x/filesystem) のいずれかにファイルを保存している場合は、`attachFromStorage` メソッドを使用してそのファイルを電子メールに添付できます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
   return $this->view('emails.orders.shipped')
               ->attachFromStorage('/path/to/file');
}
```

<!-- If necessary, you may specify the file's attachment name and additional options using the second and third arguments to the `attachFromStorage` method: -->
必要に応じて、`attachFromStorage` メソッドの 2 番目と 3 番目の引数を使用して、ファイルの添付ファイル名と追加のオプションを指定できます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
   return $this->view('emails.orders.shipped')
               ->attachFromStorage('/path/to/file', 'name.pdf', [
                   'mime' => 'application/pdf'
               ]);
}
```

<!-- The `attachFromStorageDisk` method may be used if you need to specify a storage disk other than your default disk: -->
デフォルトのディスク以外のストレージ ディスクを指定する必要がある場合は、`attachFromStorageDisk` メソッドを使用できます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
   return $this->view('emails.orders.shipped')
               ->attachFromStorageDisk('s3', '/path/to/file');
}
```

<a name="raw-data-attachments"></a>
<!-- #### Raw Data Attachments -->
#### Raw Data Attachments

<!-- The `attachData` method may be used to attach a raw string of bytes as an attachment. For example, you might use this method if you have generated a PDF in memory and want to attach it to the email without writing it to disk. The `attachData` method accepts the raw data bytes as its first argument, the name of the file as its second argument, and an array of options as its third argument: -->
`attachData` メソッドを使用して、生のバイト文字列を添付ファイルとして添付できます。たとえば、メモリ内に PDF を生成し、それをディスクに書き込まずに電子メールに添付したい場合は、この方法を使用できます。 `attachData` メソッドは、最初の引数として生データ バイト、2 番目の引数としてファイル名、3 番目の引数としてオプションの配列を受け入れます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
    return $this->view('emails.orders.shipped')
                ->attachData($this->pdf, 'name.pdf', [
                    'mime' => 'application/pdf',
                ]);
}
```

<a name="inline-attachments"></a>
<!-- ### Inline Attachments -->
### Inline Attachments

<!-- Embedding inline images into your emails is typically cumbersome; however, Laravel provides a convenient way to attach images to your emails. To embed an inline image, use the `embed` method on the `$message` variable within your email template. Laravel automatically makes the `$message` variable available to all of your email templates, so you don't need to worry about passing it in manually: -->
通常、電子メールにインライン画像を埋め込むのは面倒です。ただし、Laravel では、メールに画像を添付する便利な方法が提供されています。インライン画像を埋め込むには、電子メール テンプレート内の `$message` 変数で `embed` メソッドを使用します。 Laravel は自動的に `$message` 変数をすべての電子メール テンプレートで利用できるようにするため、手動で渡すことを心配する必要はありません。

```
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!NOTE]
> プレーン テキスト メッセージはインライン添付ファイルを利用しないため、`$message` 変数はプレーン テキスト メッセージ テンプレートでは使用できません。

<a name="embedding-raw-data-attachments"></a>
<!-- #### Embedding Raw Data Attachments -->
#### Embedding Raw Data Attachments

<!-- If you already have a raw image data string you wish to embed into an email template, you may call the `embedData` method on the `$message` variable. When calling the `embedData` method, you will need to provide a filename that should be assigned to the embedded image: -->
電子メール テンプレートに埋め込みたい生の画像データ文字列が既にある場合は、`$message` 変数で `embedData` メソッドを呼び出すことができます。 `embedData` メソッドを呼び出すときは、埋め込み画像に割り当てるファイル名を指定する必要があります。

```
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="customizing-the-swiftmailer-message"></a>
<!-- ### Customizing The SwiftMailer Message -->
### Customizing The SwiftMailer Message

<!-- The `withSwiftMessage` method of the `Mailable` base class allows you to register a closure which will be invoked with the SwiftMailer message instance before sending the message. This gives you an opportunity to deeply customize the message before it is delivered: -->
`Mailable` 基本クラスの `withSwiftMessage` メソッドを使用すると、メッセージを送信する前に SwiftMailer メッセージ インスタンスで呼び出されるクロージャーを登録できます。これにより、メッセージを配信する前に詳細にカスタマイズする機会が得られます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
    $this->view('emails.orders.shipped');

    $this->withSwiftMessage(function ($message) {
        $message->getHeaders()->addTextHeader(
            'Custom-Header', 'Header Value'
        );
    });

    return $this;
}
```

<a name="markdown-mailables"></a>
<!-- ## Markdown Mailables -->
## Markdown Mailables

<!-- Markdown mailable messages allow you to take advantage of the pre-built templates and components of [mail notifications](/docs/8.x/notifications#mail-notifications) in your mailables. Since the messages are written in Markdown, Laravel is able to render beautiful, responsive HTML templates for the messages while also automatically generating a plain-text counterpart. -->
マークダウンのメール可能メッセージを使用すると、メール可能メッセージで事前に構築されたテンプレートと [mail notifications](/docs/8.x/notifications#mail-notifications) のコンポーネントを利用できます。メッセージは Markdown で記述されているため、Laravel はメッセージ用の美しく応答性の高い HTML テンプレートをレンダリングできると同時に、対応するプレーンテキストも自動的に生成します。

<a name="generating-markdown-mailables"></a>
<!-- ### Generating Markdown Mailables -->
### Generating Markdown Mailables

<!-- To generate a mailable with a corresponding Markdown template, you may use the `--markdown` option of the `make:mail` Artisan command: -->
対応する Markdown テンプレートを使用してメール可能ファイルを生成するには、`make:mail` Artisan コマンドの `--markdown` オプションを使用できます。

```
php artisan make:mail OrderShipped --markdown=emails.orders.shipped
```

<!-- Then, when configuring the mailable within its `build` method, call the `markdown` method instead of the `view` method. The `markdown` method accepts the name of the Markdown template and an optional array of data to make available to the template: -->
次に、`build` メソッド内でメール可能ファイルを構成するときに、`view` メソッドの代わりに `markdown` メソッドを呼び出します。 `markdown` メソッドは、Markdown テンプレートの名前と、テンプレートで使用できるようにするオプションのデータ配列を受け入れます。

```
/**
 * Build the message.
 *
 * @return $this
 */
public function build()
{
    return $this->from('example@example.com')
                ->markdown('emails.orders.shipped', [
                    'url' => $this->orderUrl,
                ]);
}
```

<a name="writing-markdown-messages"></a>
<!-- ### Writing Markdown Messages -->
### Writing Markdown Messages

<!-- Markdown mailables use a combination of Blade components and Markdown syntax which allow you to easily construct mail messages while leveraging Laravel's pre-built email UI components: -->
Markdown メール可能ファイルは、Blade コンポーネントと Markdown 構文の組み合わせを使用するため、Laravel の事前構築済み電子メール UI コンポーネントを活用しながら、メール メッセージを簡単に作成できます。

```
@component('mail::message')
# Order Shipped

Your order has been shipped!

@component('mail::button', ['url' => $url])
View Order
@endcomponent

Thanks,<br>
{{ config('app.name') }}
@endcomponent
```

> [!TIP]
> Markdown メールを作成するときは、過剰なインデントを使用しないでください。 Markdown 標準に従って、Markdown パーサーはインデントされたコンテンツをコード ブロックとしてレンダリングします。

<a name="button-component"></a>
<!-- #### Button Component -->
#### Button Component

<!-- The button component renders a centered button link. The component accepts two arguments, a `url` and an optional `color`. Supported colors are `primary`, `success`, and `error`. You may add as many button components to a message as you wish: -->
ボタン コンポーネントは、中央にボタン リンクをレンダリングします。このコンポーネントは、`url` とオプションの `color` の 2 つの引数を受け入れます。サポートされている色は、`primary`、`success`、および `error` です。ボタン コンポーネントは必要なだけメッセージに追加できます。

```
@component('mail::button', ['url' => $url, 'color' => 'success'])
View Order
@endcomponent
```

<a name="panel-component"></a>
<!-- #### Panel Component -->
#### Panel Component

<!-- The panel component renders the given block of text in a panel that has a slightly different background color than the rest of the message. This allows you to draw attention to a given block of text: -->
パネル コンポーネントは、メッセージの残りの部分とはわずかに異なる背景色を持つパネルに指定されたテキスト ブロックをレンダリングします。これにより、特定のテキスト ブロックに注意を向けることができます。

```
@component('mail::panel')
This is the panel content.
@endcomponent
```

<a name="table-component"></a>
<!-- #### Table Component -->
#### Table Component

<!-- The table component allows you to transform a Markdown table into an HTML table. The component accepts the Markdown table as its content. Table column alignment is supported using the default Markdown table alignment syntax: -->
table コンポーネントを使用すると、Markdown テーブルを HTML テーブルに変換できます。コンポーネントは、Markdown テーブルをコンテンツとして受け入れます。テーブル列の配置は、デフォルトの Markdown テーブル配置構文を使用してサポートされます。

```
@component('mail::table')
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
@endcomponent
```

<a name="customizing-the-components"></a>
<!-- ### Customizing The Components -->
### Customizing The Components

<!-- You may export all of the Markdown mail components to your own application for customization. To export the components, use the `vendor:publish` Artisan command to publish the `laravel-mail` asset tag: -->
すべての Markdown メール コンポーネントを独自のアプリケーションにエクスポートしてカスタマイズできます。コンポーネントをエクスポートするには、`vendor:publish` Artisan コマンドを使用して、`laravel-mail` アセット タグを公開します。

```
php artisan vendor:publish --tag=laravel-mail
```

<!-- This command will publish the Markdown mail components to the `resources/views/vendor/mail` directory. The `mail` directory will contain an `html` and a `text` directory, each containing their respective representations of every available component. You are free to customize these components however you like. -->
このコマンドは、Markdown メール コンポーネントを `resources/views/vendor/mail` ディレクトリに公開します。 `mail` ディレクトリには、`html` ディレクトリと `text` ディレクトリが含まれ、それぞれに使用可能なすべてのコンポーネントのそれぞれの表現が含まれます。これらのコンポーネントは自由にカスタマイズできます。

<a name="customizing-the-css"></a>
<!-- #### Customizing The CSS -->
#### Customizing The CSS

<!-- After exporting the components, the `resources/views/vendor/mail/html/themes` directory will contain a `default.css` file. You may customize the CSS in this file and your styles will automatically be converted to inline CSS styles within the HTML representations of your Markdown mail messages. -->
コンポーネントをエクスポートすると、`resources/views/vendor/mail/html/themes` ディレクトリに `default.css` ファイルが含まれます。このファイル内の CSS をカスタマイズすると、スタイルは Markdown メール メッセージの HTML 表現内のインライン CSS スタイルに自動的に変換されます。

<!-- If you would like to build an entirely new theme for Laravel's Markdown components, you may place a CSS file within the `html/themes` directory. After naming and saving your CSS file, update the `theme` option of your application's `config/mail.php` configuration file to match the name of your new theme. -->
Laravel の Markdown コンポーネント用にまったく新しいテーマを構築したい場合は、CSS ファイルを `html/themes` ディレクトリ内に配置できます。 CSS ファイルに名前を付けて保存した後、アプリケーションの `config/mail.php` 構成ファイルの `theme` オプションを新しいテーマの名前と一致するように更新します。

<!-- To customize the theme for an individual mailable, you may set the `$theme` property of the mailable class to the name of the theme that should be used when sending that mailable. -->
個々のメール可能ファイルのテーマをカスタマイズするには、メール可能クラスの `$theme` プロパティを、そのメール可能ファイルの送信時に使用するテーマの名前に設定します。

<a name="sending-mail"></a>
<!-- ## Sending Mail -->
## Sending Mail

<!-- To send a message, use the `to` method on the `Mail` [facade](/docs/8.x/facades). The `to` method accepts an email address, a user instance, or a collection of users. If you pass an object or collection of objects, the mailer will automatically use their `email` and `name` properties when determining the email's recipients, so make sure these attributes are available on your objects. Once you have specified your recipients, you may pass an instance of your mailable class to the `send` method: -->
メッセージを送信するには、`Mail` [facade](/docs/8.x/facades) で `to` メソッドを使用します。 `to` メソッドは、電子メール アドレス、ユーザー インスタンス、またはユーザーのコレクションを受け入れます。オブジェクトまたはオブジェクトのコレクションを渡す場合、メーラーは電子メールの受信者を決定するときに `email` および `name` プロパティを自動的に使用するため、これらの属性がオブジェクトで使用できることを確認してください。受信者を指定したら、メール可能クラスのインスタンスを `send` メソッドに渡すことができます。

```
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
```

<!-- You are not limited to just specifying the "to" recipients when sending a message. You are free to set "to", "cc", and "bcc" recipients by chaining their respective methods together: -->
メッセージを送信するときは、受信者の「宛先」を指定するだけではありません。それぞれのメソッドを連鎖させることで、「to」、「cc」、「bcc」の受信者を自由に設定できます。

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
<!-- #### Looping Over Recipients -->
#### Looping Over Recipients

<!-- Occasionally, you may need to send a mailable to a list of recipients by iterating over an array of recipients / email addresses. However, since the `to` method appends email addresses to the mailable's list of recipients, each iteration through the loop will send another email to every previous recipient. Therefore, you should always re-create the mailable instance for each recipient: -->
場合によっては、受信者/電子メール アドレスの配列を反復処理して、受信者のリストにメール可能ファイルを送信する必要がある場合があります。ただし、`to` メソッドは電子メール アドレスをメール可能受信者のリストに追加するため、ループを繰り返すたびに、前のすべての受信者に別の電子メールが送信されます。したがって、受信者ごとにメール可能インスタンスを常に再作成する必要があります。

```
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
<!-- #### Sending Mail Via A Specific Mailer -->
#### Sending Mail Via A Specific Mailer

<!-- By default, Laravel will send email using the mailer configured as the `default` mailer in your application's `mail` configuration file. However, you may use the `mailer` method to send a message using a specific mailer configuration: -->
デフォルトでは、Laravel はアプリケーションの `mail` 設定ファイルで `default` メーラーとして設定されたメーラーを使用して電子メールを送信します。ただし、`mailer` メソッドを使用して、特定のメーラー構成を使用してメッセージを送信することもできます。

```
Mail::mailer('postmark')
        ->to($request->user())
        ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
<!-- ### Queueing Mail -->
### Queueing Mail

<a name="queueing-a-mail-message"></a>
<!-- #### Queueing A Mail Message -->
#### Queueing A Mail Message

<!-- Since sending email messages can negatively impact the response time of your application, many developers choose to queue email messages for background sending. Laravel makes this easy using its built-in [unified queue API](/docs/8.x/queues). To queue a mail message, use the `queue` method on the `Mail` facade after specifying the message's recipients: -->
電子メール メッセージの送信はアプリケーションの応答時間に悪影響を与える可能性があるため、多くの開発者はバックグラウンド送信のために電子メール メッセージをキューに入れることを選択します。 Laravel では、組み込みの [unified queue API](/docs/8.x/queues) を使用してこれを簡単に実行できます。メール メッセージをキューに入れるには、メッセージの受信者を指定した後、`Mail` ファサードで `queue` メソッドを使用します。

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

<!-- This method will automatically take care of pushing a job onto the queue so the message is sent in the background. You will need to [configure your queues](/docs/8.x/queues) before using this feature. -->
このメソッドは、ジョブをキューにプッシュする処理を自動的に処理するため、メッセージはバックグラウンドで送信されます。この機能を使用する前に、[configure your queues](/docs/8.x/queues) する必要があります。

<a name="delayed-message-queueing"></a>
<!-- #### Delayed Message Queueing -->
#### Delayed Message Queueing

<!-- If you wish to delay the delivery of a queued email message, you may use the `later` method. As its first argument, the `later` method accepts a `DateTime` instance indicating when the message should be sent: -->
キューに入れられた電子メール メッセージの配信を遅らせたい場合は、`later` メソッドを使用できます。 `later` メソッドは、最初の引数として、メッセージをいつ送信するかを示す `DateTime` インスタンスを受け取ります。

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->addMinutes(10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
<!-- #### Pushing To Specific Queues -->
#### Pushing To Specific Queues

<!-- Since all mailable classes generated using the `make:mail` command make use of the `Illuminate\Bus\Queueable` trait, you may call the `onQueue` and `onConnection` methods on any mailable class instance, allowing you to specify the connection and queue name for the message: -->
`make:mail` コマンドを使用して生成されたすべてのメール可能クラスは `Illuminate\Bus\Queueable` 特性を利用するため、任意のメール可能クラス インスタンスで `onQueue` メソッドと `onConnection` メソッドを呼び出して、メッセージの接続とキュー名を指定できます。

```
$message = (new OrderShipped($order))
                ->onConnection('sqs')
                ->onQueue('emails');

Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue($message);
```

<a name="queueing-by-default"></a>
<!-- #### Queueing By Default -->
#### Queueing By Default

<!-- If you have mailable classes that you want to always be queued, you may implement the `ShouldQueue` contract on the class. Now, even if you call the `send` method when mailing, the mailable will still be queued since it implements the contract: -->
常にキューに入れておきたいメール可能なクラスがある場合は、そのクラスに `ShouldQueue` コントラクトを実装できます。ここで、メール送信時に `send` メソッドを呼び出したとしても、メール可能ファイルはコントラクトを実装しているため、引き続きキューに入れられます。

```
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    //
}
```

<a name="queued-mailables-and-database-transactions"></a>
<!-- #### Queued Mailables & Database Transactions -->
#### Queued Mailables & Database Transactions

<!-- When queued mailables are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your mailable depends on these models, unexpected errors can occur when the job that sends the queued mailable is processed. -->
キューに入れられたメール可能ファイルがデータベース トランザクション内でディスパッチされると、データベース トランザクションがコミットされる前にキューによって処理される可能性があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに対して行った更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。メール可能ファイルがこれらのモデルに依存している場合、キューに入れられたメール可能ファイルを送信するジョブの処理時に予期しないエラーが発生する可能性があります。

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued mailable should be dispatched after all open database transactions have been committed by calling the `afterCommit` method when sending the mail message: -->
キュー接続の `after_commit` 構成オプションが `false` に設定されている場合でも、メール メッセージの送信時に `afterCommit` メソッドを呼び出して、開いているすべてのデータベース トランザクションがコミットされた後に特定のキューに入れられたメール可能ファイルをディスパッチする必要があることを指定できます。

```
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

<!-- Alternatively, you may call the `afterCommit` method from your mailable's constructor: -->
あるいは、メール可能ファイルのコンストラクターから `afterCommit` メソッドを呼び出すこともできます。

```
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
```

> [!TIP]
> これらの問題の回避方法の詳細については、[queued jobs and database transactions](/docs/8.x/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="rendering-mailables"></a>
<!-- ## Rendering Mailables -->
## Rendering Mailables

<!-- Sometimes you may wish to capture the HTML content of a mailable without sending it. To accomplish this, you may call the `render` method of the mailable. This method will return the evaluated HTML content of the mailable as a string: -->
メール可能ファイルを送信せずに、その HTML コンテンツをキャプチャしたい場合があります。これを実現するには、メール可能ファイルの `render` メソッドを呼び出します。このメソッドは、メール可能ファイルの評価された HTML コンテンツを文字列として返します。

```
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
<!-- ### Previewing Mailables In The Browser -->
### Previewing Mailables In The Browser

<!-- When designing a mailable's template, it is convenient to quickly preview the rendered mailable in your browser like a typical Blade template. For this reason, Laravel allows you to return any mailable directly from a route closure or controller. When a mailable is returned, it will be rendered and displayed in the browser, allowing you to quickly preview its design without needing to send it to an actual email address: -->
メール可能ファイルのテンプレートを設計する場合、一般的な Blade テンプレートと同様に、レンダリングされたメール可能ファイルをブラウザーですばやくプレビューできると便利です。このため、Laravel では、ルート クロージャーまたはコントローラから直接メール可能ファイルを返すことができます。メール可能ファイルが返されると、レンダリングされてブラウザに表示されるため、実際の電子メール アドレスに送信しなくても、そのデザインをすばやくプレビューできます。

```
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

> [!NOTE]
> メール可能ファイルをブラウザでプレビューする場合、[Inline attachments](#inline-attachments) はレンダリングされません。これらのメール可能ファイルをプレビューするには、[MailHog](https://github.com/mailhog/MailHog) や [HELO](https://usehelo.com) などの電子メール テスト アプリケーションに送信する必要があります。

<a name="localizing-mailables"></a>
<!-- ## Localizing Mailables -->
## Localizing Mailables

<!-- Laravel allows you to send mailables in a locale other than the request's current locale, and will even remember this locale if the mail is queued. -->
Laravel では、リクエストの現在のロケール以外のロケールでメール可能ファイルを送信することができ、メールがキューに入れられている場合でもこのロケールを記憶します。

<!-- To accomplish this, the `Mail` facade offers a `locale` method to set the desired language. The application will change into this locale when the mailable's template is being evaluated and then revert back to the previous locale when evaluation is complete: -->
これを実現するために、`Mail` ファサードは、希望の言語を設定するための `locale` メソッドを提供します。アプリケーションは、メール可能テンプレートの評価中にこのロケールに変更され、評価が完了すると前のロケールに戻ります。

```
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
<!-- ### User Preferred Locales -->
### User Preferred Locales

<!-- Sometimes, applications store each user's preferred locale. By implementing the `HasLocalePreference` contract on one or more of your models, you may instruct Laravel to use this stored locale when sending mail: -->
場合によっては、アプリケーションが各ユーザーの優先ロケールを保存することがあります。 1 つ以上のモデルに `HasLocalePreference` コントラクトを実装することで、メール送信時にこの保存されたロケールを使用するように Laravel に指示できます。

```
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
```

<!-- Once you have implemented the interface, Laravel will automatically use the preferred locale when sending mailables and notifications to the model. Therefore, there is no need to call the `locale` method when using this interface: -->
インターフェースを実装すると、Laravel はメール可能ファイルや通知をモデルに送信するときに優先ロケールを自動的に使用します。したがって、このインターフェイスを使用する場合は、`locale` メソッドを呼び出す必要はありません。

```
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
<!-- ## Testing Mailables -->
## Testing Mailables

<!-- Laravel provides several convenient methods for testing that your mailables contain the content that you expect. These methods are: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInText`, and `assertDontSeeInText`. -->
Laravel には、メール可能ファイルに期待するコンテンツが含まれていることをテストするための便利な方法がいくつか用意されています。これらのメソッドは、`assertSeeInHtml`、`assertDontSeeInHtml`、`assertSeeInText`、および `assertDontSeeInText` です。

<!-- As you might expect, the "HTML" assertions assert that the HTML version of your mailable contains a given string, while the "text" assertions assert that the plain-text version of your mailable contains a given string: -->
ご想像のとおり、「HTML」アサーションはメール可能ファイルの HTML バージョンに指定された文字列が含まれることをアサートし、「テキスト」アサーションはメール可能ファイルのプレーンテキスト バージョンに指定された文字列が含まれることをアサートします。

```
use App\Mail\InvoicePaid;
use App\Models\User;

public function test_mailable_content()
{
    $user = User::factory()->create();

    $mailable = new InvoicePaid($user);

    $mailable->assertSeeInHtml($user->email);
    $mailable->assertSeeInHtml('Invoice Paid');

    $mailable->assertSeeInText($user->email);
    $mailable->assertSeeInText('Invoice Paid');
}
```

<a name="testing-mailable-sending"></a>
<!-- #### Testing Mailable Sending -->
#### Testing Mailable Sending

<!-- We suggest testing the content of your mailables separately from your tests that assert that a given mailable was "sent" to a specific user. To learn how to test that mailables were sent, check out our documentation on the [Mail fake](/docs/8.x/mocking#mail-fake). -->
特定のメール可能ファイルが特定のユーザーに「送信された」ことを確認するテストとは別に、メール可能ファイルのコンテンツをテストすることをお勧めします。メール可能ファイルが送信されたことをテストする方法については、[Mail fake](/docs/8.x/mocking#mail-fake) のドキュメントを参照してください。

<a name="mail-and-local-development"></a>
<!-- ## Mail & Local Development -->
## Mail & Local Development

<!-- When developing an application that sends email, you probably don't want to actually send emails to live email addresses. Laravel provides several ways to "disable" the actual sending of emails during local development. -->
電子メールを送信するアプリケーションを開発する場合、実際には実際の電子メール アドレスに電子メールを送信したくないでしょう。 Laravel には、ローカル開発中に実際の電子メールの送信を「無効にする」方法がいくつか用意されています。

<a name="log-driver"></a>
<!-- #### Log Driver -->
#### Log Driver

<!-- Instead of sending your emails, the `log` mail driver will write all email messages to your log files for inspection. Typically, this driver would only be used during local development. For more information on configuring your application per environment, check out the [configuration documentation](/docs/8.x/configuration#environment-configuration). -->
電子メールを送信する代わりに、`log` メール ドライバは検査のためにすべての電子メール メッセージをログ ファイルに書き込みます。通常、このドライバはローカル開発中にのみ使用されます。環境ごとのアプリケーションの構成の詳細については、[configuration documentation](/docs/8.x/configuration#environment-configuration) を確認してください。

<a name="mailtrap"></a>
<!-- #### HELO / Mailtrap / MailHog -->
#### HELO / Mailtrap / MailHog

<!-- Alternatively, you may use a service like [HELO](https://usehelo.com) or [Mailtrap](https://mailtrap.io) and the `smtp` driver to send your email messages to a "dummy" mailbox where you may view them in a true email client. This approach has the benefit of allowing you to actually inspect the final emails in Mailtrap's message viewer. -->
あるいは、[HELO](https://usehelo.com) や [Mailtrap](https://mailtrap.io) などのサービスと `smtp` ドライバを使用して、電子メール メッセージを「ダミー」メールボックスに送信し、実際の電子メール クライアントで表示することもできます。このアプローチには、Mailtrap のメッセージ ビューアで最終的な電子メールを実際に検査できるという利点があります。

<!-- If you are using [Laravel Sail](/docs/8.x/sail), you may preview your messages using [MailHog](https://github.com/mailhog/MailHog). When Sail is running, you may access the MailHog interface at: `http://localhost:8025`. -->
[Laravel Sail](/docs/8.x/sail) を使用している場合は、[MailHog](https://github.com/mailhog/MailHog) を使用してメッセージをプレビューできます。 Sail の実行中は、`http://localhost:8025` で MailHog インターフェイスにアクセスできます。

<a name="using-a-global-to-address"></a>
<!-- #### Using A Global `to` Address -->
#### Using A Global `to` Address

<!-- Finally, you may specify a global "to" address by invoking the `alwaysTo` method offered by the `Mail` facade. Typically, this method should be called from the `boot` method of one of your application's service providers: -->
最後に、`Mail` ファサードが提供する `alwaysTo` メソッドを呼び出して、グローバル "to" アドレスを指定できます。通常、このメソッドは、アプリケーションのサービスプロバイダの 1 つの `boot` メソッドから呼び出す必要があります。

```
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
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel fires two events during the process of sending mail messages. The `MessageSending` event is fired prior to a message being sent, while the `MessageSent` event is fired after a message has been sent. Remember, these events are fired when the mail is being *sent*, not when it is queued. You may register event listeners for this event in your `App\Providers\EventServiceProvider` service provider: -->
Laravel は、メールメッセージの送信プロセス中に 2 つのイベントを発生させます。 `MessageSending` イベントはメッセージの送信前に発生しますが、`MessageSent` イベントはメッセージの送信後に発生します。これらのイベントは、メールがキューに入れられたときではなく、*送信*されたときに発生することに注意してください。 `App\Providers\EventServiceProvider` サービスプロバイダでこのイベントのイベント リスナを登録できます。

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Mail\Events\MessageSending' => [
        'App\Listeners\LogSendingMessage',
    ],
    'Illuminate\Mail\Events\MessageSent' => [
        'App\Listeners\LogSentMessage',
    ],
];
```


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
이메일을 보내는 일은 복잡할 필요가 없습니다. Laravel은 인기 있는 [SwiftMailer](https://swiftmailer.symfony.com/) 라이브러리를 기반으로 깔끔하고 단순한 이메일 API를 제공합니다. Laravel과 SwiftMailer는 SMTP, Mailgun, Postmark, Amazon SES, 그리고 `sendmail`을 통한 이메일 전송을 지원하는 다양한 드라이버(전송 방식)를 제공하여, 로컬 또는 클라우드 기반 서비스로 쉽게 메일 전송을 시작할 수 있습니다.

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Laravel's email services may be configured via your application's `config/mail.php` configuration file. Each mailer configured within this file may have its own unique configuration and even its own unique "transport", allowing your application to use different email services to send certain email messages. For example, your application might use Postmark to send transactional emails while using Amazon SES to send bulk emails. -->
Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일에서 구성할 수 있습니다. 이 파일에 등록된 각 메일러(mailers)마다 고유한 설정과 "트랜스포트(전송 방식)"를 지정할 수 있으며, 메일 종류에 따라 서로 다른 이메일 서비스를 사용할 수도 있습니다. 예를 들어, Postmark로 트랜잭션(거래) 메일을 보내고, Amazon SES로 대량 메일을 발송하는 식으로 활용할 수 있습니다.

<!-- Within your `mail` configuration file, you will find a `mailers` configuration array. This array contains a sample configuration entry for each of the major mail drivers / transports supported by Laravel, while the `default` configuration value determines which mailer will be used by default when your application needs to send an email message. -->
`mail` 설정 파일 안에서 `mailers` 설정 배열을 찾을 수 있습니다. 이 배열에는 Laravel이 지원하는 주요 메일 드라이버별 샘플 설정이 들어 있습니다. 그리고 `default` 설정 값은 이메일을 보낼 때 기본적으로 어떤 mailer가 사용될지를 결정합니다.

<a name="driver-prerequisites"></a>
<!-- ### Driver / Transport Prerequisites -->
### Driver / Transport Prerequisites

<!-- The API based drivers such as Mailgun and Postmark are often simpler and faster than sending mail via SMTP servers. Whenever possible, we recommend that you use one of these drivers. All of the API based drivers require the Guzzle HTTP library, which may be installed via the Composer package manager: -->
Mailgun이나 Postmark와 같은 API 기반 드라이버는 대개 SMTP 서버를 통한 전송보다 더 간단하고 빠릅니다. 가능하다면 이러한 드라이버 사용을 권장합니다. 모든 API 기반 드라이버는 Guzzle HTTP 라이브러리를 필요로 하며, Composer 패키지 매니저로 설치할 수 있습니다.

```
composer require guzzlehttp/guzzle
```

<a name="mailgun-driver"></a>
<!-- #### Mailgun Driver -->
#### Mailgun Driver

<!-- To use the Mailgun driver, first install the Guzzle HTTP library. Then, set the `default` option in your `config/mail.php` configuration file to `mailgun`. Next, verify that your `config/services.php` configuration file contains the following options: -->
Mailgun 드라이버를 사용하려면 먼저 Guzzle HTTP 라이브러리를 설치하십시오. 그리고 `config/mail.php` 설정 파일의 `default` 옵션을 `mailgun`으로 지정해야 합니다. 다음으로, `config/services.php` 설정 파일에 아래와 같은 옵션이 포함되어 있는지 확인합니다.

```
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
],
```

<!-- If you are not using the United States [Mailgun region](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions), you may define your region's endpoint in the `services` configuration file: -->
미국 이외의 [Mailgun region](https://documentation.mailgun.com/en/latest/api-intro.html#mailgun-regions)을 사용한다면, `services` 설정 파일에서 해당 리전의 엔드포인트를 지정할 수 있습니다.

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
Postmark 드라이버를 사용하려면, Composer를 통해 Postmark의 SwiftMailer 트랜스포트를 설치해야 합니다.

```
composer require wildbit/swiftmailer-postmark
```

<!-- Next, install the Guzzle HTTP library and set the `default` option in your `config/mail.php` configuration file to `postmark`. Finally, verify that your `config/services.php` configuration file contains the following options: -->
그 다음, Guzzle HTTP 라이브러리를 설치하고, `config/mail.php` 설정 파일의 `default` 옵션을 `postmark`로 설정합니다. 마지막으로, `config/services.php` 설정 파일에 다음 옵션이 포함되어 있어야 합니다.

```
'postmark' => [
    'token' => env('POSTMARK_TOKEN'),
],
```

<!-- If you would like to specify the Postmark message stream that should be used by a given mailer, you may add the `message_stream_id` configuration option to the mailer's configuration array. This configuration array can be found in your application's `config/mail.php` configuration file: -->
특정 mailer에서 사용할 Postmark 메시지 스트림을 지정하고 싶다면, 해당 mailer의 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다. 이 설정은 애플리케이션의 `config/mail.php` 파일 안에서 지정할 수 있습니다.

```
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
],
```

<!-- This way you are also able to set up multiple Postmark mailers with different message streams. -->
이렇게 하면 서로 다른 메시지 스트림을 사용하는 여러 Postmark mailer를 구성할 수도 있습니다.

<a name="ses-driver"></a>
<!-- #### SES Driver -->
#### SES Driver

<!-- To use the Amazon SES driver you must first install the Amazon AWS SDK for PHP. You may install this library via the Composer package manager: -->
Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. Composer 패키지 매니저로 이 라이브러리를 설치할 수 있습니다.

```bash
composer require aws/aws-sdk-php
```

<!-- Next, set the `default` option in your `config/mail.php` configuration file to `ses` and verify that your `config/services.php` configuration file contains the following options: -->
그 다음, `config/mail.php` 파일의 `default` 옵션을 `ses`로 설정하고, `config/services.php` 설정 파일에 아래 옵션들이 포함되어 있는지 확인합니다.

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

<!-- To utilize AWS [temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html) via a session token, you may add a `token` key to your application's SES configuration: -->
세션 토큰을 활용한 AWS [temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 사용하려면, 애플리케이션의 SES 설정에 `token` 키를 추가할 수 있습니다.

```
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

<!-- If you would like to define [additional options](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-email-2010-12-01.html#sendrawemail) that Laravel should pass to the AWS SDK's `SendRawEmail` method when sending an email, you may define an `options` array within your `ses` configuration: -->
또한, 이메일 발송 시 Laravel이 AWS SDK의 `SendRawEmail` 메서드에 전달해야 할 [additional options](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-email-2010-12-01.html#sendrawemail)을 지정하고 싶다면, `ses` 설정에 `options` 배열을 정의할 수 있습니다.

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
외부 서비스를 통해 애플리케이션의 메일을 전송하는 경우, 해당 서비스가 일시적으로 중단될 수 있습니다. 이런 상황에 대비해 한 개 이상의 백업 메일 전송 설정을 지정해, 주 전송 드라이버가 작동하지 않을 때 자동으로 사용할 수 있습니다.

<!-- To accomplish this, you should define a mailer within your application's `mail` configuration file that uses the `failover` transport. The configuration array for your application's `failover` mailer should contain an array of `mailers` that reference the order in which mail drivers should be chosen for delivery: -->
이를 위해, `mail` 설정 파일에서 `failover` 트랜스포트를 사용하는 mailer를 정의해야 합니다. `failover` mailer의 설정 배열에는 메일을 보낼 때 어떤 순서로 메일 드라이버를 선택할지 지정하는 `mailers` 배열이 들어가야 합니다.

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
failover mailer를 정의했다면, 이 mailer를 애플리케이션의 기본 mailer로 지정하여 `mail` 설정 파일의 `default` 키 값으로 이름을 할당합니다.

```
'default' => env('MAIL_MAILER', 'failover'),
```

<a name="generating-mailables"></a>
<!-- ## Generating Mailables -->
## Generating Mailables

<!-- When building Laravel applications, each type of email sent by your application is represented as a "mailable" class. These classes are stored in the `app/Mail` directory. Don't worry if you don't see this directory in your application, since it will be generated for you when you create your first mailable class using the `make:mail` Artisan command: -->
Laravel 애플리케이션을 개발할 때, 애플리케이션에서 발송하는 각 이메일 유형은 "메일러블(mailable)" 클래스 하나로 표현됩니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 이 디렉터리를 처음 보신다면 걱정하지 마세요. 메일러블 클래스를 `make:mail` 아티즌 명령어로 처음 생성하면 자동으로 만들어집니다.

```
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
<!-- ## Writing Mailables -->
## Writing Mailables

<!-- Once you have generated a mailable class, open it up so we can explore its contents. First, note that all of a mailable class' configuration is done in the `build` method. Within this method, you may call various methods such as `from`, `subject`, `view`, and `attach` to configure the email's presentation and delivery. -->
메일러블 클래스를 생성했으면, 해당 파일을 열고 내용을 살펴봅시다. 모든 메일러블 클래스의 설정은 `build` 메서드에서 이루어집니다. 이 메서드에서는 `from`, `subject`, `view`, `attach`와 같은 여러 메서드를 사용하여 이메일의 형태와 전송 방식을 자유롭게 설정할 수 있습니다.

> [!TIP]
> 메일러블의 `build` 메서드에서 의존성을 타입힌트로 지정할 수 있습니다. Laravel [service container](/docs/8.x/container)가 해당 의존성을 자동으로 주입해줍니다.

<a name="configuring-the-sender"></a>
<!-- ### Configuring The Sender -->
### Configuring The Sender

<a name="using-the-from-method"></a>
<!-- #### Using The `from` Method -->
#### Using The `from` Method

<!-- First, let's explore configuring the sender of the email. Or, in other words, who the email is going to be "from". There are two ways to configure the sender. First, you may use the `from` method within your mailable class' `build` method: -->
먼저, 이메일의 발신자를 설정하는 방법을 알아봅시다. 즉, 이메일이 "누구로부터 왔는가"를 지정하는 것입니다. 발신자는 두 가지 방식으로 지정할 수 있습니다. 우선, 메일러블 클래스의 `build` 메서드에서 `from` 메서드를 사용해 직접 지정할 수 있습니다.

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
하지만, 애플리케이션이 모든 이메일에 동일한 "from" 주소를 사용한다면, 생성할 때마다 `from` 메서드를 호출하는 일은 번거로울 수 있습니다. 이런 경우 `config/mail.php` 설정 파일에서 전역 "from" 주소를 지정하면, 메일러블 클래스에서 별도로 지정하지 않는 한 이 주소가 기본값으로 사용됩니다.

```
'from' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<!-- In addition, you may define a global "reply_to" address within your `config/mail.php` configuration file: -->
또한, `config/mail.php` 파일에서 전역 "reply_to" 주소도 지정할 수 있습니다.

```
'reply_to' => ['address' => 'example@example.com', 'name' => 'App Name'],
```

<a name="configuring-the-view"></a>
<!-- ### Configuring The View -->
### Configuring The View

<!-- Within a mailable class' `build` method, you may use the `view` method to specify which template should be used when rendering the email's contents. Since each email typically uses a [Blade template](/docs/8.x/blade) to render its contents, you have the full power and convenience of the Blade templating engine when building your email's HTML: -->
메일러블 클래스의 `build` 메서드에서 `view` 메서드를 사용해 이메일 본문의 템플릿을 지정할 수 있습니다. 이메일 본문은 보통 [Blade template](/docs/8.x/blade)을 사용하므로, Blade 템플릿 엔진의 강력한 기능을 모두 활용할 수 있습니다.

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
> 이메일용 템플릿을 보관하려면 `resources/views/emails` 디렉터리를 별도로 만드시는 것도 좋습니다. 물론, 필요하다면 `resources/views` 디렉터리의 원하는 위치에 저장할 수 있습니다.

<a name="plain-text-emails"></a>
<!-- #### Plain Text Emails -->
#### Plain Text Emails

<!-- If you would like to define a plain-text version of your email, you may use the `text` method. Like the `view` method, the `text` method accepts a template name which will be used to render the contents of the email. You are free to define both an HTML and plain-text version of your message: -->
이메일의 일반 텍스트 버전을 따로 정의하고 싶다면, `text` 메서드를 사용할 수 있습니다. `view` 메서드처럼 `text` 메서드도 이메일 내용을 렌더링하는 데 사용할 템플릿 이름을 받습니다. HTML과 일반 텍스트 버전을 모두 설정할 수도 있습니다.

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
일반적으로, 이메일 본문을 랜더링할 때 템플릿에서 사용할 데이터를 전달하고 싶을 때가 많습니다. 뷰에 데이터를 전달하는 방법은 두 가지가 있습니다. 첫 번째 방법은, 메일러블 클래스에 퍼블릭 속성(public property)을 정의하면 자동으로 해당 데이터가 뷰에 전달됩니다. 예를 들어, 생성자에서 데이터를 받아 퍼블릭 속성에 할당할 수 있습니다.

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
퍼블릭 속성에 데이터를 할당하면, 해당 데이터가 자동으로 뷰에 전달되어 Blade 템플릿에서 일반 데이터처럼 사용할 수 있습니다.

```
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-method"></a>
<!-- #### Via The `with` Method: -->
#### Via The `with` Method:

<!-- If you would like to customize the format of your email's data before it is sent to the template, you may manually pass your data to the view via the `with` method. Typically, you will still pass data via the mailable class' constructor; however, you should set this data to `protected` or `private` properties so the data is not automatically made available to the template. Then, when calling the `with` method, pass an array of data that you wish to make available to the template: -->
이메일 데이터의 포맷을 템플릿에 보내기 전에 직접 지정하고 싶다면, `with` 메서드를 사용해 데이터를 전달할 수 있습니다. 이 경우 데이터는 메일러블 클래스의 생성자를 통해 받은 뒤, `protected`나 `private` 속성으로 저장하면 해당 데이터가 기본적으로 템플릿에 노출되지 않습니다. 그 다음, `with` 메서드에 템플릿에 전달할 데이터 배열을 지정합니다.

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
`with` 메서드로 데이터를 전달하면 해당 데이터 역시 뷰에서 쉽게 사용할 수 있습니다.

```
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
<!-- ### Attachments -->
### Attachments

<!-- To add attachments to an email, use the `attach` method within the mailable class' `build` method. The `attach` method accepts the full path to the file as its first argument: -->
이메일에 첨부 파일을 추가하려면, 메일러블 클래스의 `build` 메서드에서 `attach` 메서드를 사용합니다. `attach` 메서드는 첫 번째 인자로 첨부할 파일의 전체 경로를 받습니다.

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
파일을 첨부할 때, `attach` 메서드의 두 번째 인자로 `array`를 전달하여 파일의 표시 이름이나 MIME 타입을 지정할 수도 있습니다.

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
파일이 [filesystem disks](/docs/8.x/filesystem) 중 하나에 저장되어 있다면, `attachFromStorage` 메서드를 사용해 첨부할 수 있습니다.

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
필요하다면, `attachFromStorage` 메서드의 두 번째, 세 번째 인자로 파일의 첨부 이름이나 추가 옵션을 지정할 수 있습니다.

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
기본 디스크가 아닌 다른 스토리지 디스크를 지정해야 한다면, `attachFromStorageDisk` 메서드를 사용할 수 있습니다.

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
`attachData` 메서드는 바이트 문자열 데이터를 첨부 파일로 추가할 때 사용합니다. 예를 들어, PDF 파일을 메모리상에서 생성하고 디스크에 저장하지 않은 채 첨부하고 싶은 경우에 적합합니다. `attachData` 메서드는 첫 번째 인자로 원시 데이터, 두 번째 인자로 파일 이름, 세 번째 인자로 옵션 배열을 받습니다.

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
이메일에 이미지를 인라인으로 삽입하는 일은 일반적으로 번거롭지만, Laravel은 이를 쉽게 할 수 있는 방법을 제공합니다. 인라인 이미지를 첨부하려면, 이메일 템플릿에서 `$message` 변수의 `embed` 메서드를 사용하세요. Laravel은 모든 이메일 템플릿에 `$message` 변수를 자동으로 전달하므로, 따로 전달할 필요가 없습니다.

```
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!NOTE]
> `$message` 변수는 플레인 텍스트 메일 템플릿에서는 사용할 수 없습니다. 플레인 텍스트에는 인라인 첨부 기능이 적용되지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
<!-- #### Embedding Raw Data Attachments -->
#### Embedding Raw Data Attachments

<!-- If you already have a raw image data string you wish to embed into an email template, you may call the `embedData` method on the `$message` variable. When calling the `embedData` method, you will need to provide a filename that should be assigned to the embedded image: -->
이미 원시 이미지 데이터 문자열이 있다면, `$message` 변수의 `embedData` 메서드로 해당 이미지를 템플릿에 임베드할 수 있습니다. `embedData` 메서드를 호출할 때는 임베드할 이미지에 지정할 파일 이름도 함께 전달해야 합니다.

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
`Mailable` 베이스 클래스의 `withSwiftMessage` 메서드를 사용하면, 메일 발송 직전에 SwiftMailer 메시지 인스턴스를 가지고 원하는 커스터마이징을 수행할 수 있습니다. 이 메서드에 클로저를 전달하면, 해당 클로저에서 메시지를 직접 다룰 수 있습니다.

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
마크다운 메일러블(Markdown mailables)을 사용하면 [mail notifications](/docs/8.x/notifications#mail-notifications)의 미리 만들어진 템플릿 및 컴포넌트의 이점을 메일러블에도 그대로 활용할 수 있습니다. 메시지는 마크다운으로 작성되며, Laravel이 이를 아름답고 반응형인 HTML 템플릿으로 렌더링해주고, 동시에 자동으로 일반 텍스트 버전도 생성합니다.

<a name="generating-markdown-mailables"></a>
<!-- ### Generating Markdown Mailables -->
### Generating Markdown Mailables

<!-- To generate a mailable with a corresponding Markdown template, you may use the `--markdown` option of the `make:mail` Artisan command: -->
마크다운 템플릿과 함께 메일러블을 생성하려면, `make:mail` 아티즌 명령어의 `--markdown` 옵션을 사용합니다.

```
php artisan make:mail OrderShipped --markdown=emails.orders.shipped
```

<!-- Then, when configuring the mailable within its `build` method, call the `markdown` method instead of the `view` method. The `markdown` method accepts the name of the Markdown template and an optional array of data to make available to the template: -->
이후 메일러블의 `build` 메서드에서 `view` 대신 `markdown` 메서드를 사용하십시오. `markdown` 메서드는 첫 번째 인자로 마크다운 템플릿 이름을, 두 번째 인자로 템플릿에 전달할 선택적 데이터 배열을 받습니다.

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
마크다운 메일러블은 Blade 컴포넌트와 마크다운 구문을 조합하여, Laravel이 제공하는 이메일 UI 컴포넌트들을 활용하면서 메일 메시지를 쉽게 작성할 수 있습니다.

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
> 마크다운 이메일을 작성할 때는 들여쓰기를 과하게 사용하지 마세요. 마크다운 표준에 따라, 들여쓰기된 내용은 코드 블록으로 처리될 수 있습니다.

<a name="button-component"></a>
<!-- #### Button Component -->
#### Button Component

<!-- The button component renders a centered button link. The component accepts two arguments, a `url` and an optional `color`. Supported colors are `primary`, `success`, and `error`. You may add as many button components to a message as you wish: -->
버튼 컴포넌트는 중앙에 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적인 `color` 두 인자를 받습니다. 지원되는 색상은 `primary`, `success`, `error`이며, 한 메시지에 버튼 컴포넌트를 여러 개 추가할 수도 있습니다.

```
@component('mail::button', ['url' => $url, 'color' => 'success'])
View Order
@endcomponent
```

<a name="panel-component"></a>
<!-- #### Panel Component -->
#### Panel Component

<!-- The panel component renders the given block of text in a panel that has a slightly different background color than the rest of the message. This allows you to draw attention to a given block of text: -->
패널 컴포넌트는 지정된 텍스트 블록을 나머지 메시지와는 살짝 다른 배경색의 패널로 표시해줍니다. 특정 문구에 시선을 집중시키고 싶을 때 유용합니다.

```
@component('mail::panel')
This is the panel content.
@endcomponent
```

<a name="table-component"></a>
<!-- #### Table Component -->
#### Table Component

<!-- The table component allows you to transform a Markdown table into an HTML table. The component accepts the Markdown table as its content. Table column alignment is supported using the default Markdown table alignment syntax: -->
테이블 컴포넌트를 사용하면 마크다운 테이블을 HTML 테이블로 변환할 수 있습니다. 이 컴포넌트는 마크다운 테이블을 콘텐츠로 받으며, 기본적인 마크다운 표 정렬 문법을 그대로 지원합니다.

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
모든 마크다운 메일 컴포넌트를 여러분의 애플리케이션 내에서 커스터마이징하여 사용할 수 있습니다. 컴포넌트를 내보내려면, `laravel-mail` 에셋 태그를 이용해 `vendor:publish` 아티즌 명령어를 실행하십시오.

```
php artisan vendor:publish --tag=laravel-mail
```

<!-- This command will publish the Markdown mail components to the `resources/views/vendor/mail` directory. The `mail` directory will contain an `html` and a `text` directory, each containing their respective representations of every available component. You are free to customize these components however you like. -->
이 명령어를 실행하면 마크다운 메일 컴포넌트가 `resources/views/vendor/mail` 디렉터리에 복제됩니다. 이 `mail` 디렉터리에는 각각의 컴포넌트에 대한 표현이 담긴 `html` 디렉터리와 `text` 디렉터리가 포함되어 있으므로, 원하는 대로 커스터마이징할 수 있습니다.

<a name="customizing-the-css"></a>
<!-- #### Customizing The CSS -->
#### Customizing The CSS

<!-- After exporting the components, the `resources/views/vendor/mail/html/themes` directory will contain a `default.css` file. You may customize the CSS in this file and your styles will automatically be converted to inline CSS styles within the HTML representations of your Markdown mail messages. -->
컴포넌트를 내보내면 `resources/views/vendor/mail/html/themes` 경로에 `default.css` 파일이 생성됩니다. 이 파일 내 CSS를 수정하면, 수정 내용이 HTML 메일의 인라인 CSS 스타일로 자동 변환되어 적용됩니다.

<!-- If you would like to build an entirely new theme for Laravel's Markdown components, you may place a CSS file within the `html/themes` directory. After naming and saving your CSS file, update the `theme` option of your application's `config/mail.php` configuration file to match the name of your new theme. -->
Laravel의 마크다운 컴포넌트용으로 완전히 새로운 테마를 만들고 싶다면, CSS 파일을 `html/themes` 디렉터리 내에 직접 생성할 수도 있습니다. CSS 파일의 이름을 정한 뒤 저장한 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 `theme` 옵션 값을 새 테마 이름으로 지정하면 됩니다.

<!-- To customize the theme for an individual mailable, you may set the `$theme` property of the mailable class to the name of the theme that should be used when sending that mailable. -->
특정 개별 메일러블에만 커스텀 테마를 적용하려면, 해당 메일러블 클래스의 `$theme` 속성을 사용해 테마명을 지정할 수 있습니다.

<a name="sending-mail"></a>
<!-- ## Sending Mail -->
## Sending Mail

<!-- To send a message, use the `to` method on the `Mail` [facade](/docs/8.x/facades). The `to` method accepts an email address, a user instance, or a collection of users. If you pass an object or collection of objects, the mailer will automatically use their `email` and `name` properties when determining the email's recipients, so make sure these attributes are available on your objects. Once you have specified your recipients, you may pass an instance of your mailable class to the `send` method: -->
메일을 보내려면, `Mail` [facade](/docs/8.x/facades)에서 `to` 메서드를 사용합니다. `to` 메서드는 이메일 주소, 사용자 인스턴스, 또는 사용자 컬렉션을 받을 수 있습니다. 객체나 객체의 컬렉션을 전달하면, 메일러가 자동으로 해당 객체의 `email` 및 `name` 속성을 참조해 수신자를 결정합니다. 수신자를 지정한 후, 메일러블 클래스 인스턴스를 `send` 메서드에 전달하면 됩니다.

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
메일 전송 시, "to"(받는 사람)만 지정할 필요는 없습니다. "cc", "bcc"를 포함한 여러 수신자를 메서드 체이닝 방식으로 추가 지정할 수도 있습니다.

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
가끔 여러 명의 수신자(또는 이메일 주소)에 메일러블을 반복적으로 보내야 할 때가 있습니다. 하지만 `to` 메서드는 수신자 리스트에 이메일 주소를 추가하는 방식이므로, 반복문에서 같은 인스턴스를 여러 번 사용하면, 이전까지의 모든 수신자에게 메일이 계속 중복 발송됩니다. 이런 경우에는 매 반복마다 새 메일러블 인스턴스를 생성해야 합니다.

```
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
<!-- #### Sending Mail Via A Specific Mailer -->
#### Sending Mail Via A Specific Mailer

<!-- By default, Laravel will send email using the mailer configured as the `default` mailer in your application's `mail` configuration file. However, you may use the `mailer` method to send a message using a specific mailer configuration: -->
기본적으로 Laravel은 애플리케이션의 `mail` 설정 파일에 `default` mailer로 설정된 메일러를 사용해 메일을 전송합니다. 하지만, `mailer` 메서드를 사용하면, 특정 mailer 설정을 사용해 메일을 보낼 수도 있습니다.

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
이메일 전송으로 인해 애플리케이션의 응답 속도가 느려질 수 있으므로, 상당수 개발자는 이메일을 백그라운드에서 전송하도록 큐에 쌓는 방식을 선호합니다. Laravel은 [unified queue API](/docs/8.x/queues)를 통해 이를 손쉽게 구현할 수 있습니다. 메일 메시지를 큐에 넣으려면, 수신자 지정 후 `Mail` 퍼사드의 `queue` 메서드를 사용합니다.

```
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

<!-- This method will automatically take care of pushing a job onto the queue so the message is sent in the background. You will need to [configure your queues](/docs/8.x/queues) before using this feature. -->
이 메서드는 메일이 백그라운드에서 발송될 수 있도록 큐에 자동으로 작업을 추가합니다. 이 기능을 사용하려면 [configure your queues](/docs/8.x/queues)을 먼저 완료해야 합니다.

<a name="delayed-message-queueing"></a>
<!-- #### Delayed Message Queueing -->
#### Delayed Message Queueing

<!-- If you wish to delay the delivery of a queued email message, you may use the `later` method. As its first argument, the `later` method accepts a `DateTime` instance indicating when the message should be sent: -->
큐에 넣은 메일의 발송을 일정 시간 지연시키고 싶을 때는, `later` 메서드를 사용할 수 있습니다. `later` 메서드는 첫 번째 인자로 언제 보낼지 지정하는 `DateTime` 인스턴스를 받습니다.

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
`make:mail` 명령어로 생성된 모든 메일러블 클래스에는 `Illuminate\Bus\Queueable` 트레이트가 포함되어 있습니다. 이 덕분에, 메일러블 인스턴스의 `onQueue`, `onConnection` 메서드를 통해, 전송할 큐와 연결명을 자유롭게 지정할 수 있습니다.

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
항상 큐를 통해 전송되길 원하는 메일러블 클래스라면, 클래스에서 `ShouldQueue` 계약(Contract)을 구현하면 됩니다. 이렇게 하면 `send` 메서드로 보낼 때도 자동으로 큐에 들어갑니다.

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
큐에 쌓인 메일러블이 데이터베이스 트랜잭션 도중에 디스패치 되면, 큐에서 작업이 처리되는 시점에 아직 트랜잭션이 완료되지 않았을 수 있습니다. 이 경우 트랜잭션 내에서 변경된 모델이나 데이터가 데이터베이스에 반영되지 않았거나, 트랜잭션 내에서 새로 생성된 레코드가 아직 없을 수도 있습니다. 그래서 메일러블이 해당 모델이나 레코드를 필요로 하는 경우, 큐 작업 실행 중 예기치 못한 오류가 발생할 수 있습니다.

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued mailable should be dispatched after all open database transactions have been committed by calling the `afterCommit` method when sending the mail message: -->
만약 큐 연결의 `after_commit` 설정이 `false`로 되어 있다면, `afterCommit` 메서드를 호출해 메일 메시지를 데이터베이스 트랜잭션 커밋 이후에 디스패치되도록 지정할 수 있습니다.

```
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

<!-- Alternatively, you may call the `afterCommit` method from your mailable's constructor: -->
또는, 메일러블의 생성자 내부에서 `afterCommit` 메서드를 호출할 수도 있습니다.

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
> 이러한 문제를 우회하는 방법에 대해 더 자세히 알아보려면 [queued jobs and database transactions](/docs/8.x/queues#jobs-and-database-transactions) 문서를 참고하십시오.

<a name="rendering-mailables"></a>
<!-- ## Rendering Mailables -->
## Rendering Mailables

<!-- Sometimes you may wish to capture the HTML content of a mailable without sending it. To accomplish this, you may call the `render` method of the mailable. This method will return the evaluated HTML content of the mailable as a string: -->
어떤 경우에는 메일러블을 실제로 발송하지 않고, HTML 콘텐츠만 별도로 얻고 싶을 때가 있습니다. 이럴 때는 메일러블의 `render` 메서드를 호출하면, 평가된 HTML 콘텐츠를 문자열로 반환합니다.

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
메일러블의 템플릿을 디자인할 때, 일반 Blade 템플릿처럼 브라우저에서 결과를 빠르게 미리 보고 싶을 때가 있습니다. 이런 경우, Laravel에서는 라우트 클로저나 컨트롤러에서 메일러블을 직접 반환하게 하면, 실제 이메일 주소로 메일을 보내지 않고 브라우저에서 바로 렌더링 결과를 확인할 수 있습니다.

```
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

> [!NOTE]
> [Inline attachments](#inline-attachments)은 브라우저에서 미리볼 때는 렌더링되지 않습니다. 이러한 메일을 미리보기 위해서는 [MailHog](https://github.com/mailhog/MailHog)이나 [HELO](https://usehelo.com)와 같은 이메일 테스트 애플리케이션에 실제로 전송해야 합니다.

<a name="localizing-mailables"></a>
<!-- ## Localizing Mailables -->
## Localizing Mailables

<!-- Laravel allows you to send mailables in a locale other than the request's current locale, and will even remember this locale if the mail is queued. -->
Laravel은 현재 요청의 로케일(locale)과 다른 언어로 메일러블을 전송할 수 있으며, 메일이 큐에 들어가도 이 로케일이 기억됩니다.

<!-- To accomplish this, the `Mail` facade offers a `locale` method to set the desired language. The application will change into this locale when the mailable's template is being evaluated and then revert back to the previous locale when evaluation is complete: -->
이를 위해, `Mail` 퍼사드의 `locale` 메서드를 사용해 원하는 언어를 지정할 수 있습니다. 메일러블의 템플릿이 렌더링되는 동안만 해당 로케일로 전환되며, 렌더링이 끝나면 원래 로케일로 다시 돌아옵니다.

```
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
<!-- ### User Preferred Locales -->
### User Preferred Locales

<!-- Sometimes, applications store each user's preferred locale. By implementing the `HasLocalePreference` contract on one or more of your models, you may instruct Laravel to use this stored locale when sending mail: -->
가끔 애플리케이션은 각 사용자의 선호 로케일을 별도로 저장할 때가 있습니다. 이런 경우, 한 개 이상의 모델에 `HasLocalePreference` 계약을 구현하면, Laravel이 자동으로 이 값을 읽어 메일 전송 시 사용합니다.

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
이 인터페이스를 구현하면, Laravel이 해당 모델에 메일러블이나 알림을 전송할 때 자동으로 선호 로케일을 적용합니다. 따라서 `locale` 메서드를 별도로 호출할 필요가 없습니다.

```
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
<!-- ## Testing Mailables -->
## Testing Mailables

<!-- Laravel provides several convenient methods for testing that your mailables contain the content that you expect. These methods are: `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInText`, and `assertDontSeeInText`. -->
Laravel은 메일러블이 기대한 내용을 포함하는지 테스트할 수 있도록 여러 편리한 메서드를 제공합니다. 대표적으로 `assertSeeInHtml`, `assertDontSeeInHtml`, `assertSeeInText`, `assertDontSeeInText`가 있습니다.

<!-- As you might expect, the "HTML" assertions assert that the HTML version of your mailable contains a given string, while the "text" assertions assert that the plain-text version of your mailable contains a given string: -->
"HTML" 어서션은 메일러블의 HTML 버전에 특정 문자열이 있는지 검증하고, "text" 어서션은 일반 텍스트 버전에 원하는 문자열이 있는지 검증합니다.

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
메일러블의 "발송" 자체를 확인하는 테스트와, 메일러블의 콘텐츠 테스트는 별도로 작성하는 것을 권장합니다. 실제로 메일러블이 발송되었는지 테스트하려면 [Mail fake](/docs/8.x/mocking#mail-fake) 관련 문서를 참고해 주세요.

<a name="mail-and-local-development"></a>
<!-- ## Mail & Local Development -->
## Mail & Local Development

<!-- When developing an application that sends email, you probably don't want to actually send emails to live email addresses. Laravel provides several ways to "disable" the actual sending of emails during local development. -->
이메일을 보내는 애플리케이션을 개발할 때, 실제 이메일 주소로 실제 메일을 전송하고 싶지는 않을 것입니다. Laravel은 로컬 환경에서 이메일의 실제 전송을 "비활성화"할 수 있는 여러 기능을 제공합니다.

<a name="log-driver"></a>
<!-- #### Log Driver -->
#### Log Driver

<!-- Instead of sending your emails, the `log` mail driver will write all email messages to your log files for inspection. Typically, this driver would only be used during local development. For more information on configuring your application per environment, check out the [configuration documentation](/docs/8.x/configuration#environment-configuration). -->
이메일을 실제로 발송하는 대신, `log` 메일 드라이버는 모든 이메일 내용을 로그 파일에 기록하여 확인할 수 있게 해줍니다. 보통 이 드라이버는 로컬 개발 환경에서만 사용합니다. 환경별 애플리케이션 설정 방법은 [configuration documentation](/docs/8.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
<!-- #### HELO / Mailtrap / MailHog -->
#### HELO / Mailtrap / MailHog

<!-- Alternatively, you may use a service like [HELO](https://usehelo.com) or [Mailtrap](https://mailtrap.io) and the `smtp` driver to send your email messages to a "dummy" mailbox where you may view them in a true email client. This approach has the benefit of allowing you to actually inspect the final emails in Mailtrap's message viewer. -->
또는 [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io) 같은 서비스와 `smtp` 드라이버를 함께 써서, 실제 메일함이 아닌 "더미" 메일함에 메시지를 전송하고, 실제 이메일 클라이언트에서 확인할 수도 있습니다. 이 방법의 장점은 최종 이메일을 Mailtrap의 메시지 뷰어 등에서 실제로 살펴볼 수 있다는 점입니다.

<!-- If you are using [Laravel Sail](/docs/8.x/sail), you may preview your messages using [MailHog](https://github.com/mailhog/MailHog). When Sail is running, you may access the MailHog interface at: `http://localhost:8025`. -->
[Laravel Sail](/docs/8.x/sail)을 사용한다면, [MailHog](https://github.com/mailhog/MailHog)를 통해 메시지를 미리볼 수도 있습니다. Sail이 실행 중인 동안에는 `http://localhost:8025`에서 MailHog 인터페이스에 접속할 수 있습니다.

<a name="using-a-global-to-address"></a>
<!-- #### Using A Global `to` Address -->
#### Using A Global `to` Address

<!-- Finally, you may specify a global "to" address by invoking the `alwaysTo` method offered by the `Mail` facade. Typically, this method should be called from the `boot` method of one of your application's service providers: -->
마지막으로, `Mail` 퍼사드의 `alwaysTo` 메서드를 통해 "전역 to 주소"를 지정할 수도 있습니다. 이 메서드는 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출합니다.

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
Laravel은 메일 메시지 전송 과정에서 두 가지 이벤트를 발생시킵니다. 메일 전송 전에 `MessageSending` 이벤트가, 전송 후에는 `MessageSent` 이벤트가 트리거됩니다. 이 이벤트들은 메일이 실제로 *발송*될 때 발생하며, 큐에 들어갈 때는 발생하지 않습니다. `App\Providers\EventServiceProvider` 서비스 프로바이더에서 이 이벤트의 리스너를 등록할 수 있습니다.

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

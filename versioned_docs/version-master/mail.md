# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 / 전송 방식 사전 준비](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드 로빈(round robin) 설정](#round-robin-configuration)
- [메일러블 생성하기](#generating-mailables)
- [메일러블 작성하기](#writing-mailables)
    - [발신자 설정](#configuring-the-sender)
    - [뷰(View) 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부 파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그 및 메타데이터](#tags-and-metadata)
    - [Symfony 메일 메시지 커스터마이징](#customizing-the-symfony-message)
- [Markdown 메일러블](#markdown-mailables)
    - [Markdown 메일러블 생성](#generating-markdown-mailables)
    - [Markdown 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [메일 보내기](#sending-mail)
    - [메일 큐잉 처리](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 지역화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 내용 테스트](#testing-mailable-content)
    - [메일러블 전송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송 방식](#custom-transports)
    - [추가 Symfony 전송 방식](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 전송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 한 간결하고 직관적인 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, 그리고 `sendmail` 등 다양한 전송 드라이버를 지원하므로, 로컬 또는 클라우드 기반 서비스 중 원하는 것으로 쉽고 빠르게 메일 전송을 시작할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에 설정된 각 메일러(mailers)는 고유의 설정, 그리고 고유한 "전송 방식(transport)"을 가질 수 있습니다. 이렇게 하면 특정 메일러로는 트랜잭션 이메일, 다른 메일러로는 대량 이메일 등 서로 다른 이메일을 목적에 맞는 서비스로 보낼 수 있습니다.

`mail` 설정 파일 안에는 `mailers` 설정 배열이 있습니다. 이 배열은 Laravel에서 지원하는 주요 메일 드라이버 및 전송 방식 샘플이 담겨 있으며, `default` 설정 값은 애플리케이션에서 메일을 보낼 때 기본적으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송 방식 사전 준비 (Driver / Transport Prerequisites)

Mailgun, Postmark, Resend 등과 같은 API 기반 드라이버는 대개 SMTP 서버를 사용하는 것보다 간단하고 더 빠릅니다. 가능하다면 이러한 드라이버 사용을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 Symfony의 Mailgun Mailer transport를 Composer로 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

다음으로, 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지를 변경해야 합니다. 먼저, 기본 메일러를 `mailgun`으로 설정합니다:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

그리고, 다음 설정 배열을 `mailers` 배열에 추가합니다:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러 설정을 마친 후, `config/services.php` 파일에도 다음 옵션을 추가해야 합니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 Mailgun 리전([Mailgun region](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions))을 사용하지 않는 경우, 리전에 맞는 endpoint를 `services` 설정 파일에 지정할 수 있습니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
    'scheme' => 'https',
],
```

<a name="postmark-driver"></a>
#### Postmark 드라이버

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면 Symfony의 Postmark Mailer transport를 Composer로 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그리고 `config/mail.php`에서 `default` 옵션을 `postmark`로 설정하세요. 이후, `config/services.php` 파일에 다음 옵션이 있는지 확인합니다:

```php
'postmark' => [
    'key' => env('POSTMARK_API_KEY'),
],
```

특정 메일러에 사용할 Postmark 메시지 스트림을 지정하려면 설정 배열에 `message_stream_id` 옵션을 추가합니다. 이 배열은 `config/mail.php` 파일에 위치합니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이 방식으로 서로 다른 메시지 스트림을 가진 여러 Postmark 메일러를 설정할 수도 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Resend의 PHP SDK를 Composer로 설치하세요:

```shell
composer require resend/resend-php
```

그리고 `config/mail.php` 파일에서 `default` 옵션을 `resend`로 설정합니다. 이후, `config/services.php` 파일에 다음 옵션이 있는지 확인하세요:

```php
'resend' => [
    'key' => env('RESEND_API_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 Composer로 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

그 다음 `config/mail.php` 파일에서 `default` 옵션을 `ses`로, 그리고 `config/services.php` 파일에 아래와 같은 옵션이 있는지 확인합니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS의 [임시 자격 증명(temporary credentials)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 사용하려면, SES 설정에 `token` 키를 추가합니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리(subscription management)](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html) 기능을 사용하려면, 메일 메시지의 [headers](#headers) 메서드에서 반환되는 배열에 `X-Ses-List-Management-Options` 헤더를 추가하세요:

```php
/**
 * Get the message headers.
 */
public function headers(): Headers
{
    return new Headers(
        text: [
            'X-Ses-List-Management-Options' => 'contactListName=MyContactList;topicName=MyTopic',
        ],
    );
}
```

Laravel이 AWS SDK의 `SendEmail` 메서드에 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 지정하려면, `ses` 설정에 `options` 배열을 추가할 수 있습니다:

```php
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
```

<a name="failover-configuration"></a>
### 장애 조치(failover) 설정 (Failover Configuration)

외부 서비스를 통해 메일을 전송할 때 서비스가 일시적으로 다운될 수 있습니다. 이럴 때를 대비해, 기본 메일러가 비활성일 경우 사용할 백업 메일러(장애 조치)를 미리 정의해 두면 안전합니다.

이를 위해, `mail` 설정 파일 내에 `failover` 전송 방식을 사용하는 메일러를 정의하세요. `failover` 메일러의 설정 배열에는 사용할 메일러 순서대로 `mailers` 배열을 넣습니다:

```php
'mailers' => [
    'failover' => [
        'transport' => 'failover',
        'mailers' => [
            'postmark',
            'mailgun',
            'sendmail',
        ],
        'retry_after' => 60,
    ],

    // ...
],
```

장애 조치 메일러를 설정했다면, `.env` 파일에서 기본 메일러를 다음과 같이 변경합니다:

```ini
MAIL_MAILER=failover
```

<a name="round-robin-configuration"></a>
### 라운드 로빈(round robin) 설정 (Round Robin Configuration)

`roundrobin` 전송 방식은 여러 메일러로 메일 발송 작업을 분산 처리할 수 있게 해줍니다. 이를 위해, `mail` 설정 파일에 `roundrobin` 전송 방식을 사용하는 메일러를 정의하세요. 설정 배열의 `mailers`에는 분산 처리에 사용할 메일러들을 나열합니다:

```php
'mailers' => [
    'roundrobin' => [
        'transport' => 'roundrobin',
        'mailers' => [
            'ses',
            'postmark',
        ],
        'retry_after' => 60,
    ],

    // ...
],
```

라운드 로빈 메일러를 정의했다면, `mail` 설정 파일의 `default` 항목에서 이 메일러를 기본값으로 지정합니다:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 전송 방식은 설정된 목록에서 무작위로 메일러를 선택한 뒤, 다음 메일 전송 때는 순차적으로 또 다른 메일러를 사용합니다. 이는 장애 조치(`failover`)가 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)*를 제공하는 것과 달리, 라운드 로빈은 *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))*을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 생성하기 (Generating Mailables)

Laravel 애플리케이션에서는 각 이메일 유형을 "메일러블(mailable)" 클래스로 구현합니다. 이 클래스들은 `app/Mail` 디렉터리에 저장됩니다. 만약 해당 디렉터리가 없다면, `make:mail` Artisan 명령어로 첫 메일러블 클래스를 생성할 때 자동으로 만들어집니다:

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성하기 (Writing Mailables)

메일러블 클래스를 생성했다면, 해당 파일을 열어 내용을 살펴봅니다. 메일러블 클래스는 주로 `envelope`, `content`, `attachments` 등의 메서드로 구성하며, 각각 이메일의 제목, 수신자, 뷰 등 주요 속성을 정의합니다.

`envelope` 메서드는 메시지의 제목과, (필요하다면) 수신자를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성하는 데 사용할 [Blade 템플릿](/docs/master/blade) 등 정보를 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 설정 (Configuring the Sender)

<a name="using-the-envelope"></a>
#### Envelope로 발신자 지정

이메일의 발신자(From)를 설정하는 방법을 알아보겠습니다. 발신자는 두 가지 방식으로 지정할 수 있습니다.

첫 번째 방법은, 메시지의 envelope에서 "from" 주소를 지정하는 것입니다:

```php
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Envelope;

/**
 * Get the message envelope.
 */
public function envelope(): Envelope
{
    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        subject: 'Order Shipped',
    );
}
```

필요하다면 `replyTo` 주소도 지정할 수 있습니다:

```php
return new Envelope(
    from: new Address('jeffrey@example.com', 'Jeffrey Way'),
    replyTo: [
        new Address('taylor@example.com', 'Taylor Otwell'),
    ],
    subject: 'Order Shipped',
);
```

<a name="using-a-global-from-address"></a>
#### 글로벌 "from" 주소 사용하기

애플리케이션 전체 메일 발신자가 항상 동일하다면, 메일러블마다 설정하는 대신 `config/mail.php` 파일에 글로벌 "from" 주소를 지정할 수 있습니다. 메일러블에서 별도로 "from" 주소를 지정하지 않으면 이 값이 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한 글로벌 "reply_to" 주소도 아래와 같이 지정할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰(View) 설정 (Configuring the View)

메일러블 클래스의 `content` 메서드에서 어떤 뷰(템플릿)를 활용해 이메일을 렌더링할지 정의할 수 있습니다. 대부분의 이메일은 [Blade 템플릿](/docs/master/blade)을 활용하여 내용을 작성하므로, Blade의 강력한 기능과 편리함을 그대로 누릴 수 있습니다:

```php
/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
    );
}
```

> [!NOTE]
> 모든 이메일 템플릿을 위한 `resources/views/mail` 디렉터리를 따로 만들어 관리할 것을 권장하지만, 실제로는 `resources/views` 내 원하는 위치에 배치해도 됩니다.

<a name="plain-text-emails"></a>
#### 평문 텍스트 이메일

이메일의 평문(plain-text) 버전을 따로 정의하고 싶다면, 메시지의 `Content` 정의 시 `text` 파라미터에 평문 템플릿 이름을 지정하면 됩니다. 이렇게 하면 HTML과 텍스트 버전을 모두 제공할 수 있습니다:

```php
/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
        text: 'mail.orders.shipped-text'
    );
}
```

좀 더 명확하게 하려면 `html` 파라미터를 `view`의 별칭으로 활용할 수도 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터 (View Data)

<a name="via-public-properties"></a>
#### public 속성을 통한 전달

템플릿에서 활용할 데이터를 뷰로 전달하는 방법은 두 가지가 있습니다. 첫 번째는, 메일러블 클래스에 정의된 **모든 public 속성**이 자동으로 뷰에서 접근 가능하다는 점을 활용하는 방법입니다. 데이터를 생성자에서 받아와 public 속성에 할당하면 됩니다:

```php
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
     * Create a new message instance.
     */
    public function __construct(
        public Order $order,
    ) {}

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }
}
```

데이터가 public 속성에 할당되면, Blade 템플릿에서 곧바로 접근하고 활용할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 전달

메일 데이터의 형식을 커스터마이즈해서 템플릿에 전달하고 싶을 경우, `Content` 정의의 `with` 파라미터를 통해 데이터를 명시적으로 넘길 수 있습니다. 보통은 생성자에서 데이터를 받아오고, 이 데이터를 protected 또는 private 속성에 저장합니다. public 속성이 아니기 때문에 자동 전달되지 않으니, 커스텀 가공이 가능합니다:

```php
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
     * Create a new message instance.
     */
    public function __construct(
        protected Order $order,
    ) {}

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
            with: [
                'orderName' => $this->order->name,
                'orderPrice' => $this->order->price,
            ],
        );
    }
}
```

`with` 파라미터로 전달한 데이터 역시 Blade 템플릿에서 바로 사용할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일 (Attachments)

이메일에 첨부 파일을 추가하려면, 메시지의 `attachments` 메서드에서 파일을 반환하는 배열을 작성합니다. 기본적으로 `Attachment` 클래스의 `fromPath` 메서드를 통해 파일 경로를 지정해 첨부할 수 있습니다:

```php
use Illuminate\Mail\Mailables\Attachment;

/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromPath('/path/to/file'),
    ];
}
```

첨부 파일에 별도의 표시 이름이나 MIME 타입을 지정하려면, `as` 및 `withMime` 메서드를 사용할 수 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromPath('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a name="attaching-files-from-disk"></a>
#### 디스크에서 첨부

[파일 시스템 디스크](/docs/master/filesystem)에 저장된 파일을 첨부하려면, `fromStorage` 메서드를 사용할 수 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file'),
    ];
}
```

이때도 마찬가지로 첨부 파일 이름이나 MIME 타입을 지정할 수 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

기본이 아닌 다른 스토리지 디스크를 사용해야 한다면 `fromStorageDisk` 메서드를 활용하세요:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorageDisk('s3', '/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a name="raw-data-attachments"></a>
#### 원시 데이터(바이트) 첨부

`fromData` 메서드를 사용하면, 메모리 내의 원시 바이트 데이터를 바로 첨부할 수 있습니다. 예를 들어, 메모리상에서 PDF를 생성한 후 바로 첨부하고 싶다면 이 방법이 유용합니다. `fromData` 메서드는 데이터 바이트를 반환하는 클로저와 첨부 파일의 이름을 파라미터로 받습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromData(fn () => $this->pdf, 'Report.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a name="inline-attachments"></a>
### 인라인 첨부 파일 (Inline Attachments)

HTML 이메일에 인라인 이미지를 임베드하는 일은 비교적 번거로울 수 있으나, Laravel에서는 `$message` 변수의 `embed` 메서드를 통해 손쉽게 이미지를 첨부할 수 있습니다. `$message` 변수는 모든 이메일 템플릿에서 자동으로 제공되므로 별도로 전달하지 않아도 됩니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 평문(plain-text) 메시지 템플릿에서는 제공되지 않습니다. 평문 이메일에는 인라인 첨부 기능을 쓸 수 없습니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 인라인 첨부

만약 이미 메모리 내에 원시 이미지 데이터가 있다면, `$message`의 `embedData` 메서드로 인라인 삽입할 수 있습니다. 이때 첨부할 파일의 이름도 지정해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체 (Attachable Objects)

경로 문자열 대신, 애플리케이션 내의 객체(예: `Photo` 모델)를 첨부 파일로 다루고 싶을 때도 있습니다. 이때는 파일 첨부 자체를 객체로 표현하는 것이 편리합니다.

먼저, 첨부를 원하는 클래스에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하고, `toMailAttachment` 메서드에서 `Illuminate\Mail\Attachment` 인스턴스를 반환합니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * Get the attachable representation of the model.
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

이제 이메일 메시지 작성 시 `attachments` 메서드에서 해당 객체를 배열로 반환하면 바로 첨부로 처리됩니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [$this->photo];
}
```

첨부 데이터가 Amazon S3 등 원격 파일 시스템에 저장된 경우에도, Laravel의 [파일 시스템 디스크](/docs/master/filesystem)를 활용해 인스턴스를 생성할 수 있습니다:

```php
// 기본 디스크에서 파일 첨부 생성
return Attachment::fromStorage($this->path);

// 특정 디스크에서 파일 첨부 생성
return Attachment::fromStorageDisk('backblaze', $this->path);
```

또한, 메모리상의 데이터로부터 첨부 인스턴스를 만들려면, `fromData` 메서드에 클로저를 전달하세요. 클로저는 첨부할 데이터의 바이트값을 반환해야 합니다:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부의 파일명이나 MIME 타입을 지정하고 싶을 때는, `as` 및 `withMime` 메서드를 활용할 수 있습니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더 (Headers)

때로는 아웃바운드 메시지에 Message-Id 같이 커스텀 헤더나 임의의 텍스트 헤더를 추가하고 싶을 수 있습니다.

이럴 때는 메일러블에서 `headers` 메서드를 정의하여 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환하면 됩니다. 이 클래스는 `messageId`, `references`, `text` 세 가지 파라미터를 지원하며, 필요한 부분만 지정하면 됩니다:

```php
use Illuminate\Mail\Mailables\Headers;

/**
 * Get the message headers.
 */
public function headers(): Headers
{
    return new Headers(
        messageId: 'custom-message-id@example.com',
        references: ['previous-message@example.com'],
        text: [
            'X-Custom-Header' => 'Custom Value',
        ],
    );
}
```

<a name="tags-and-metadata"></a>
### 태그 및 메타데이터 (Tags and Metadata)

Mailgun, Postmark 등 일부 외부 이메일 공급자에서는 "태그(tag)"와 "메타데이터(metadata)"를 활용해 이메일을 그룹 관리, 추적할 수 있습니다. 메일러블의 `Envelope` 정의에서 태그 및 메타데이터를 추가할 수 있습니다:

```php
use Illuminate\Mail\Mailables\Envelope;

/**
 * Get the message envelope.
 *
 * @return \Illuminate\Mail\Mailables\Envelope
 */
public function envelope(): Envelope
{
    return new Envelope(
        subject: 'Order Shipped',
        tags: ['shipment'],
        metadata: [
            'order_id' => $this->order->id,
        ],
    );
}
```

Mailgun 드라이버를 사용하는 경우 [tags](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags), [metadata](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages) 문서를 참고하세요. Postmark도 마찬가지로 [tags](https://postmarkapp.com/blog/tags-support-for-smtp), [metadata](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 문서를 참고하세요.

Amazon SES를 사용할 때는, `metadata` 메서드로 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 붙일 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메일 메시지 커스터마이징 (Customizing the Symfony Message)

Laravel의 메일 기능은 Symfony Mailer를 기반으로 동작합니다. Laravel에서는 메시지가 전송되기 전, Symfony Message 인스턴스에 대해 직접 커스텀 콜백을 등록할 수 있습니다. 이로써 메시지가 전송되기 전에 직접 내용을 커스터마이즈할 수 있습니다. 이를 위해 `Envelope` 정의의 `using` 파라미터에 콜백 배열을 추가합니다:

```php
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * Get the message envelope.
 */
public function envelope(): Envelope
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
```

<a name="markdown-mailables"></a>
## Markdown 메일러블 (Markdown Mailables)

Markdown 메일러블 메시지는 [메일 알림](/docs/master/notifications#mail-notifications)의 미리 만들어진 템플릿·컴포넌트를 메일러블에서 활용할 수 있게 해줍니다. Markdown 문법을 사용하여 작성된 메시지는 Laravel이 자동으로 보기 좋은 반응형 HTML로 렌더링하며, 동시에 평문 버전도 만들어줍니다.

<a name="generating-markdown-mailables"></a>
### Markdown 메일러블 생성 (Generating Markdown Mailables)

Markdown 템플릿과 함께 메일러블을 생성하려면, `make:mail` Artisan 명령어의 `--markdown` 옵션을 사용합니다:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

이후, 메일러블의 `content` 메서드에서 `view` 대신 `markdown` 파라미터를 사용하여 Content를 정의합니다:

```php
use Illuminate\Mail\Mailables\Content;

/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        markdown: 'mail.orders.shipped',
        with: [
            'url' => $this->orderUrl,
        ],
    );
}
```

<a name="writing-markdown-messages"></a>
### Markdown 메시지 작성 (Writing Markdown Messages)

Markdown 메일러블은 Blade 컴포넌트와 Markdown 문법의 조합으로, 미리 만들어진 UI 컴포넌트를 활용해 이메일 메시지를 쉽게 구성할 수 있습니다:

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

> [!NOTE]
> Markdown 이메일을 작성할 때는 들여쓰기를 과하게 사용하지 마세요. Markdown 표준상 들여쓰기가 많은 부분은 코드 블록으로 렌더링됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙에 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적으로 `color`(primary, success, error)를 인자로 받습니다. 원하는 만큼 여러 개의 버튼을 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 주어진 텍스트 블록을 약간 다른 배경의 패널로 표시해, 특정 영역에 시선을 집중시킬 수 있도록 해줍니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 Markdown 테이블을 HTML 테이블로 변환해줍니다. 컴포넌트의 콘텐츠로 Markdown 테이블을 그대로 삽입하면 되고, 열 정렬도 기본 Markdown 문법을 그대로 활용할 수 있습니다:

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이징 (Customizing the Components)

Laravel의 Markdown 메일 컴포넌트들을 직접 수정하고 싶을 때, 다음 Artisan 명령어로 컴포넌트를 애플리케이션으로 복사(export)할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령으로 컴포넌트들은 `resources/views/vendor/mail` 디렉터리에 복사됩니다. `mail` 디렉터리에는 `html`과 `text` 폴더가 있으며, 각각의 컴포넌트 HTML/텍스트 버전이 들어 있습니다. 마음껏 수정해 활용할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이징

컴포넌트 export 후에는 `resources/views/vendor/mail/html/themes` 디렉터리에 `default.css` 파일도 함께 생깁니다. 여기에 원하는 CSS를 추가하세요. 자동으로 각 마크다운 메일의 인라인 스타일로 변환되어 반영됩니다.

만약 완전히 새로운 테마를 만들고 싶다면 CSS 파일을 `html/themes` 아래에 생성한 뒤, `config/mail.php` 파일의 `theme` 옵션을 해당 CSS 파일명으로 지정하면 됩니다.

특정 메일러블에만 독자 테마를 적용하고 싶다면, 메일러블 클래스의 `$theme` 속성에 테마명을 입력하세요.

<a name="sending-mail"></a>
## 메일 보내기 (Sending Mail)

메시지를 보내려면 [Facade](/docs/master/facades)인 `Mail`의 `to` 메서드를 사용하세요. `to` 메서드는 이메일 주소, 사용자 인스턴스, 혹은 사용자 컬렉션을 인자로 받을 수 있습니다. 객체나 컬렉션을 전달하면, 해당 객체의 `email` 및 `name` 속성을 자동으로 수신자 정보로 사용합니다.

수신자를 지정한 뒤에는, 메일러블 클래스 인스턴스를 `send` 메서드에 전달하여 보냅니다:

```php
<?php

namespace App\Http\Controllers;

use App\Mail\OrderShipped;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;

class OrderShipmentController extends Controller
{
    /**
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Ship the order...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```

메일을 보낼 때 "to" 이외에도, "cc"와 "bcc"도 메서드 체이닝으로 추가할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 여러 수신자 반복 전송

여러 명의 수신자에게 각각 메일을 따로 보내고 싶을 때는, 반드시 반복문 내에서 **새로운 메일러블 인스턴스**를 만들어야 합니다. 그렇지 않으면 이전 모든 수신자에게 중복 발송되는 문제가 발생할 수 있습니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 통한 메일 전송

Laravel은 기본적으로 `mail.php`의 `default` 메일러를 사용하지만, `mailer` 메서드로 특정 메일러를 지정해 사용할 수도 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉 처리 (Queueing Mail)

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐에 넣기

이메일 전송이 응답 속도를 떨어뜨릴 수 있기 때문에, 많은 개발자들이 이메일을 백그라운드에서 보내기 위해 [통합 큐 API](/docs/master/queues)를 사용합니다. 메일 메시지를 큐에 넣으려면, 수신자 지정 뒤에 `queue` 메서드를 사용합니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

이렇게 하면 자동으로 큐 작업이 생성되어 백그라운드에서 메일이 전송됩니다. 이 기능을 사용하려면 [큐 환경 구성](/docs/master/queues)이 필요합니다.

<a name="delayed-message-queueing"></a>
#### 지연된 메일 큐잉

메일 발송을 일정 시간 뒤로 지연하고 싶다면, `later` 메서드를 사용하세요. 첫 번째 인자로 `DateTime` 인스턴스를 받아, 언제 발송할지 지정합니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->plus(minutes: 10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐 및 연결 지정

`make:mail`로 생성하는 모든 메일러블에는 `Illuminate\Bus\Queueable` 트레이트가 기본 포함되므로, 어떤 큐 연결(connection) 및 큐 이름(queue)을 사용할지 `onQueue`, `onConnection` 메서드로 지정할 수 있습니다:

```php
$message = (new OrderShipped($order))
    ->onConnection('sqs')
    ->onQueue('emails');

Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue($message);
```

<a name="queueing-by-default"></a>
#### 기본적으로 큐에 넣기

항상 큐를 사용하는 메일러블을 원한다면, 클래스에 `ShouldQueue` 계약을 구현하세요. 이러면 `send` 메서드를 사용하더라도 무조건 큐 처리가 됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐 메일러블과 데이터베이스 트랜잭션

큐에 올라간 메일러블이 데이터베이스 트랜잭션 내에서 디스패치될 경우, 트랜잭션이 커밋되기 전에 큐에서 작업이 처리될 여지가 있습니다. 이때, 트랜잭션 내에서 추가 또는 변경된 데이터가 아직 실제 데이터베이스에 반영되지 않았을 수 있으니 주의가 필요합니다.

큐 연결의 `after_commit` 옵션이 `false`로 되어 있다면, 메일 전송 시 `afterCommit` 메서드를 호출해 **모든 트랜잭션 커밋 이후에** 큐로 보내도록 할 수 있습니다:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는 메일러블 생성자 내부에서 `afterCommit`을 호출할 수도 있습니다:

```php
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
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이 이슈에 대한 대처법은 [큐 작업과 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐 마일러블 전송 실패 처리

큐에 올라간 이메일 전송이 실패했을 때, 해당 메일러블 클래스에 정의된 `failed` 메서드가 호출됩니다. 실패 원인이 된 `Throwable` 인스턴스가 파라미터로 전달됩니다:

```php
<?php

namespace App\Mail;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;
use Throwable;

class OrderDelayed extends Mailable implements ShouldQueue
{
    use SerializesModels;

    /**
     * Handle a queued email's failure.
     */
    public function failed(Throwable $exception): void
    {
        // ...
    }
}
```

<a name="rendering-mailables"></a>
## 메일러블 렌더링 (Rendering Mailables)

메일러블의 HTML 내용을 미리 결과만 받아보고 싶을 때, 메일러블의 `render` 메서드를 호출하면 해당 HTML을 문자열로 반환받을 수 있습니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 미리보기

템플릿을 개발하면서 메일러블을 브라우저에서 바로 확인하고 싶을 때, 라우트 클로저나 컨트롤러에서 메일러블 인스턴스를 그대로 반환하면 자동으로 렌더링되어 빠르게 결과를 확인할 수 있습니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 지역화 (Localizing Mailables)

Laravel에서는 기본 로케일이 아닌 다른 언어로 메일러블을 보내는 기능을 제공합니다. 이때 메일이 큐에 담겼더라도 로케일 정보를 함께 기억합니다.

`Mail` 파사드의 `locale` 메서드를 사용하면, 해당 메일이 렌더링될 때만 원하는 로케일로 변경 후 자동으로 원래 로케일로 복구합니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일 사용

사용자마다 선호하는 언어가 따로 저장된 경우, 모델에 `HasLocalePreference` 계약을 구현하면, 메일러블이나 알림(notification) 전송 시 자동으로 해당 로케일을 사용하게 할 수 있습니다:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * Get the user's preferred locale.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

이 인터페이스를 구현한 뒤에는, 개별적으로 `locale` 메서드를 호출할 필요 없이 바로 메일러블을 보낼 수 있습니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 내용 테스트 (Testing Mailable Content)

Laravel은 메일러블 구조와 내용을 검증할 수 있는 다양한 메서드를 제공합니다. 다음과 같이 메일러블의 다양한 속성, 포함 여부 등을 검증할 수 있습니다:

```php tab=Pest
use App\Mail\InvoicePaid;
use App\Models\User;

test('mailable content', function () {
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
    $mailable->assertDontSeeInHtml('Invoice Not Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertDontSeeInText('Invoice Not Paid');
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
});
```

```php tab=PHPUnit
use App\Mail\InvoicePaid;
use App\Models\User;

public function test_mailable_content(): void
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
    $mailable->assertDontSeeInHtml('Invoice Not Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertDontSeeInText('Invoice Not Paid');
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
}
```

여기서 "HTML" 검증 메서드는 HTML 버전 메일러블을, "text" 검증 메서드는 평문 버전 메일러블을 대상으로 합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 전송 테스트 (Testing Mailable Sending)

메일러블의 콘텐츠를 검증하는 테스트와, 메일이 특정 사용자에게 **정말로 전송(혹은 큐로 등록) 되었는지**를 검증하는 테스트는 분리하는 것이 좋습니다. 보통 메일의 상세 콘텐츠는 관심사가 아니라, **특정 메일러블이 전송 지시됨**만 확인하면 충분하기 때문입니다.

`Mail` 파사드의 `fake` 메서드를 사용하면 실제 메일 발송 없이 테스트를 제어할 수 있습니다. 이후 `assertSent`, `assertQueued` 등 다양한 메서드로 전송/큐잉 여부를 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // Perform order shipping...

    // Assert that no mailables were sent...
    Mail::assertNothingSent();

    // Assert that a mailable was sent...
    Mail::assertSent(OrderShipped::class);

    // Assert a mailable was sent twice...
    Mail::assertSent(OrderShipped::class, 2);

    // Assert a mailable was sent to an email address...
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // Assert a mailable was sent to multiple email addresses...
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // Assert a mailable was not sent...
    Mail::assertNotSent(AnotherMailable::class);

    // Assert a mailable was sent twice...
    Mail::assertSentTimes(OrderShipped::class, 2);

    // Assert 3 total mailables were sent...
    Mail::assertSentCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Mail::fake();

        // Perform order shipping...

        // Assert that no mailables were sent...
        Mail::assertNothingSent();

        // Assert that a mailable was sent...
        Mail::assertSent(OrderShipped::class);

        // Assert a mailable was sent twice...
        Mail::assertSent(OrderShipped::class, 2);

        // Assert a mailable was sent to an email address...
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // Assert a mailable was sent to multiple email addresses...
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // Assert a mailable was not sent...
        Mail::assertNotSent(AnotherMailable::class);

        // Assert a mailable was sent twice...
        Mail::assertSentTimes(OrderShipped::class, 2);

        // Assert 3 total mailables were sent...
        Mail::assertSentCount(3);
    }
}
```

백그라운드 큐로 메일러블을 보낸 경우는 `assertSent` 대신 `assertQueued`를 사용하세요:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

전체 전송/큐잉된 메일러블 개수를 검사하려면 `assertOutgoingCount` 메서드를 사용합니다:

```php
Mail::assertOutgoingCount(3);
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 등에는 클로저를 전달할 수 있습니다. 클로저 내에서 원하는 조건을 직접 검사할 수 있고, 적어도 하나가 통과하면 성공으로 처리됩니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

클로저가 받는 메일러블 인스턴스는 여러 검사 메서드를 제공합니다:

```php
Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...') &&
           $mail->hasMetadata('order_id', $mail->order->id);
           $mail->usesMailer('ses');
});
```

첨부 파일 관련 검사 메서드도 지원합니다:

```php
use Illuminate\Mail\Mailables\Attachment;

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {
    return $mail->hasAttachment(
        Attachment::fromPath('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf')
    );
});

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {
    return $mail->hasAttachment(
        Attachment::fromStorageDisk('s3', '/path/to/file')
    );
});

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($pdfData) {
    return $mail->hasAttachment(
        Attachment::fromData(fn () => $pdfData, 'name.pdf')
    );
});
```

메일이 아예 전송 또는 큐 등록이 없는 경우를 확실히 검증하고 싶으면 `assertNothingOutgoing`, 특정 조건을 부정하려면 `assertNotOutgoing`을 사용하세요:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경 (Mail and Local Development)

개발 환경에서는 실 이메일 주소로 메일을 보내고 싶지 않은 경우가 많습니다. Laravel은 로컬 개발 중에는 실제 이메일 전송을 "비활성화"할 수 있는 다양한 방법을 제공합니다.

<a name="log-driver"></a>
#### Log 드라이버

`log` 메일 드라이버를 사용하면, 모든 이메일 메시지가 로그 파일에 기록되어 실제로 전송되지 않으니 안심하고 검토할 수 있습니다. 환경별로 설정을 분리하는 방법은 [환경 설정 문서](/docs/master/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는 [HELO](https://usehelo.com)나 [Mailtrap](https://mailtrap.io) 등의 서비스, 그리고 `smtp` 드라이버를 사용해 이메일을 "더미 메일박스"로 전송할 수도 있습니다. 이 방식은 실제 이메일 클라이언트에서 발송 결과를 눈으로 직접 검수할 수 있다는 장점이 있습니다.

[Laravel Sail](/docs/master/sail) 환경에서는 [Mailpit](https://github.com/axllent/mailpit)을 활용해 전송 결과를 확인할 수 있습니다. Sail이 실행 중일 때 `http://localhost:8025`에서 Mailpit 인터페이스를 사용할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 글로벌 "to" 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 활용해 모든 메일이 특정 이메일 주소로 가도록 할 수 있습니다. 애플리케이션의 서비스 프로바이더의 `boot` 메서드에서 다음처럼 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Mail;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    if ($this->app->environment('local')) {
        Mail::alwaysTo('taylor@example.com');
    }
}
```

`alwaysTo`를 사용하면, CC/BCC 등 추가 수신자 정보도 모두 제거됩니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel은 메일 메시지를 전송하는 과정에서 두 가지 이벤트를 발생시킵니다. 메시지가 전송되기 **전**에는 `MessageSending`, 전송된 **후**에는 `MessageSent` 이벤트가 디스패치됩니다. 이 이벤트들은 메일이 **큐잉될 때가 아니라** 실제로 *전송될 때* 발생함에 유의하세요. 애플리케이션에서 [이벤트 리스너](/docs/master/events)를 정의해 활용할 수 있습니다:

```php
use Illuminate\Mail\Events\MessageSending;
// use Illuminate\Mail\Events\MessageSent;

class LogMessage
{
    /**
     * Handle the event.
     */
    public function handle(MessageSending $event): void
    {
        // ...
    }
}
```

<a name="custom-transports"></a>
## 커스텀 전송 방식 (Custom Transports)

Laravel은 다양한 메일 전송 방식을 기본으로 지원하지만, 직접 커스텀 transport를 구현해 지원되지 않는 타사 서비스로 메일을 보낼 수도 있습니다. 이를 위해서는 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 확장해 클래스를 만들고, `doSend`, `__toString` 메서드를 구현하세요:

```php
<?php

namespace App\Mail;

use MailchimpTransactional\ApiClient;
use Symfony\Component\Mailer\SentMessage;
use Symfony\Component\Mailer\Transport\AbstractTransport;
use Symfony\Component\Mime\Address;
use Symfony\Component\Mime\MessageConverter;

class MailchimpTransport extends AbstractTransport
{
    /**
     * Create a new Mailchimp transport instance.
     */
    public function __construct(
        protected ApiClient $client,
    ) {
        parent::__construct();
    }

    /**
     * {@inheritDoc}
     */
    protected function doSend(SentMessage $message): void
    {
        $email = MessageConverter::toEmail($message->getOriginalMessage());

        $this->client->messages->send(['message' => [
            'from_email' => $email->getFrom(),
            'to' => collect($email->getTo())->map(function (Address $email) {
                return ['email' => $email->getAddress(), 'type' => 'to'];
            })->all(),
            'subject' => $email->getSubject(),
            'text' => $email->getTextBody(),
        ]]);
    }

    /**
     * Get the string representation of the transport.
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```

커스텀 transport를 구현했다면, `Mail` 파사드의 `extend` 메서드로 등록합니다. 일반적으로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 처리하면 됩니다. 이때 `$config` 파라미터로는 해당 메일러의 `config/mail.php` 파일 내 설정 배열이 전달됩니다:

```php
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;
use MailchimpTransactional\ApiClient;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('mailchimp', function (array $config = []) {
        $client = new ApiClient;

        $client->setApiKey($config['key']);

        return new MailchimpTransport($client);
    });
}
```

등록이 끝나면, `config/mail.php` 내 메일러 정의에서 새 transport를 사용할 수 있습니다:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송 방식 (Additional Symfony Transports)

Laravel은 Mailgun, Postmark 등 일부 Symfony 공식 메일러 전송 방식도 지원하지만, 필요에 따라 다른 Symfony 메일러를 직접 추가로 사용할 수도 있습니다. Composer로 패키지를 설치한 뒤, Laravel에 직접 등록하면 됩니다.

예시: "Brevo"(이전 이름 Sendinblue) Symfony 메일러 활용

```shell
composer require symfony/brevo-mailer symfony/http-client
```

설치 후, 애플리케이션 `services` 설정 파일에 Brevo API 자격 정보를 입력합니다:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

그리고 서드파티 transport를 등록합니다. 주로 서비스 프로바이더의 `boot` 메서드에서 처리합니다:

```php
use Illuminate\Support\Facades\Mail;
use Symfony\Component\Mailer\Bridge\Brevo\Transport\BrevoTransportFactory;
use Symfony\Component\Mailer\Transport\Dsn;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('brevo', function () {
        return (new BrevoTransportFactory)->create(
            new Dsn(
                'brevo+api',
                'default',
                config('services.brevo.key')
            )
        );
    });
}
```

등록이 끝나면, `config/mail.php`에 새 transport로 메일러를 정의할 수 있습니다:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```

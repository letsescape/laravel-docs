# 메일 (Mail)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 조건](#driver-prerequisites)
    - [장애 조치(failover) 설정](#failover-configuration)
    - [라운드 로빈(round robin) 설정](#round-robin-configuration)
- [메일러블 생성](#generating-mailables)
- [메일러블 작성](#writing-mailables)
    - [보낸 사람 설정](#configuring-the-sender)
    - [뷰 설정](#configuring-the-view)
    - [뷰 데이터](#view-data)
    - [첨부 파일](#attachments)
    - [인라인 첨부 파일](#inline-attachments)
    - [Attachable 객체](#attachable-objects)
    - [헤더](#headers)
    - [태그와 메타데이터](#tags-and-metadata)
    - [Symfony 메시지 커스텀](#customizing-the-symfony-message)
- [Markdown 메일러블](#markdown-mailables)
    - [Markdown 메일러블 생성](#generating-markdown-mailables)
    - [Markdown 메시지 작성](#writing-markdown-messages)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [메일 발송](#sending-mail)
    - [메일 큐잉](#queueing-mail)
- [메일러블 렌더링](#rendering-mailables)
    - [브라우저에서 메일러블 미리보기](#previewing-mailables-in-the-browser)
- [메일러블 현지화](#localizing-mailables)
- [테스트](#testing-mailables)
    - [메일러블 콘텐츠 테스트](#testing-mailable-content)
    - [메일러블 발송 테스트](#testing-mailable-sending)
- [메일과 로컬 개발 환경](#mail-and-local-development)
- [이벤트](#events)
- [커스텀 전송 방식(Transport)](#custom-transports)
    - [추가 Symfony 전송 방식](#additional-symfony-transports)

<a name="introduction"></a>
## 소개 (Introduction)

이메일 발송은 복잡할 필요가 없습니다. Laravel은 인기 있는 [Symfony Mailer](https://symfony.com/doc/current/mailer.html) 컴포넌트를 기반으로 깔끔하고 간단한 이메일 API를 제공합니다. Laravel과 Symfony Mailer는 SMTP, Mailgun, Postmark, Resend, Amazon SES, `sendmail`을 통한 메일 전송 드라이버를 지원하므로, 로컬 또는 클라우드 기반 메일 서비스로 손쉽게 메일을 발송할 수 있습니다.

<a name="configuration"></a>
### 설정

Laravel의 이메일 서비스는 애플리케이션의 `config/mail.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일에서 설정한 각 메일러는 고유한 설정 및 전송 방식(transport)을 가질 수 있으며, 필요에 따라 서로 다른 메일러를 사용해 특정 이메일을 보낼 수 있습니다. 예를 들어, Postmark를 통해 트랜잭션 메일을, Amazon SES를 통해 대량 메일을 보내도록 설정할 수 있습니다.

`mail` 설정 파일에는 `mailers` 설정 배열이 있습니다. 이 배열에는 Laravel이 지원하는 주요 메일 드라이버 및 전송 방식의 샘플 구성이 포함되어 있습니다. 그리고 `default` 설정 값은 애플리케이션이 이메일을 보낼 때 기본으로 사용할 메일러를 결정합니다.

<a name="driver-prerequisites"></a>
### 드라이버 / 전송 방식 사전 조건

Mailgun, Postmark, Resend와 같이 API 기반의 드라이버는 보통 SMTP 서버를 통한 메일 전송보다 더 간단하고 빠릅니다. 가능하면 이러한 드라이버 중 하나를 사용하는 것을 권장합니다.

<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면, Composer로 Symfony의 Mailgun Mailer transport를 설치해야 합니다.

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 두 가지를 변경해야 합니다. 첫째, 기본 메일러를 `mailgun`으로 설정합니다.

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

둘째, 다음 설정 배열을 `mailers` 배열에 추가합니다.

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

기본 메일러를 설정한 후, `config/services.php` 설정 파일에도 다음 옵션을 추가합니다.

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

미국 이외의 [Mailgun 리전](https://documentation.mailgun.com/docs/mailgun/api-reference/#mailgun-regions)을 사용하는 경우, 해당 리전의 endpoint를 `services` 설정 파일에 지정할 수 있습니다.

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

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면, Composer로 Symfony의 Postmark Mailer transport를 설치하세요.

```shell
composer require symfony/postmark-mailer symfony/http-client
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `postmark`로 설정합니다. 또한, `config/services.php` 설정 파일에 다음 옵션이 포함되어 있는지 확인하세요.

```php
'postmark' => [
    'key' => env('POSTMARK_API_KEY'),
],
```

특정 메일러에서 사용할 Postmark 메시지 스트림을 지정하려면, 해당 메일러의 설정 배열에 `message_stream_id` 옵션을 추가할 수 있습니다. 이 설정 배열은 `config/mail.php` 파일에서 찾을 수 있습니다.

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

이 방식으로 서로 다른 메시지 스트림을 가진 여러 Postmark 메일러도 구성할 수 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면 Composer로 Resend의 PHP SDK를 설치하세요.

```shell
composer require resend/resend-php
```

그 다음, 애플리케이션의 `config/mail.php` 설정 파일의 `default` 옵션을 `resend`로 설정합니다. 그리고 `config/services.php` 설정 파일에 다음 옵션이 포함되어 있는지 확인하세요.

```php
'resend' => [
    'key' => env('RESEND_API_KEY'),
],
```

<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 Amazon AWS SDK for PHP를 설치해야 합니다. 이 라이브러리는 Composer로 설치할 수 있습니다.

```shell
composer require aws/aws-sdk-php
```

그리고 `config/mail.php` 설정 파일의 `default` 옵션을 `ses`로 설정하고, `config/services.php` 파일에 다음 옵션들이 있는지 반드시 확인하세요.

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)도 사용할 수 있으며, 이 경우 SES 설정에 `token` 키를 추가할 수 있습니다.

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)과 상호작용하려면, 메일 메시지의 [headers](#headers) 메서드에서 반환하는 배열에 `X-Ses-List-Management-Options` 헤더를 추가하면 됩니다.

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

Laravel이 AWS SDK의 `SendEmail` 메서드로 전달할 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 지정하려면, `ses` 설정 내에 `options` 배열을 정의할 수 있습니다.

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
### 장애 조치(failover) 설정

외부 서비스를 통해 메일을 전송하도록 설정한 경우, 외부 서비스가 다운되는 상황이 발생할 수 있습니다. 이런 상황에서는, 주 메일 전송 드라이버에 장애가 발생한 경우를 대비해 하나 이상의 백업 메일 전송 구성을 정의하는 것이 유용합니다.

이를 위해, 애플리케이션의 `mail` 설정 파일에 `failover` 전송 방식을 사용하는 메일러를 정의하면 됩니다. `failover` 메일러의 설정 배열에는 사용할 메일러의 선택 순서를 정의하는 `mailers` 배열을 포함해야 합니다.

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

이렇게 `failover` 전송 방식을 사용하는 메일러를 구성했다면, `.env` 파일에서 기본 메일러로 `failover`를 지정해야 장애 조치 기능을 사용할 수 있습니다.

```ini
MAIL_MAILER=failover
```

<a name="round-robin-configuration"></a>
### 라운드 로빈(round robin) 설정

`roundrobin` 전송 방식은 메일 발송 작업을 여러 메일러에 분산시켜줍니다. 사용하려면, `mail` 설정 파일에 `roundrobin` 전송 방식을 사용하는 메일러를 정의하면 됩니다. 이 메일러의 설정 배열에는 실제 전송에 사용할 메일러 목록을 `mailers` 배열 형태로 넣습니다.

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

라운드 로빈 메일러를 정의한 뒤, 애플리케이션의 `mail` 설정 파일에서 기본 메일러를 해당 라운드 로빈 메일러로 지정하세요.

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

라운드 로빈 전송 방식은 구성된 메일러 목록에서 임의의 메일러를 선택한 후, 이후 메일마다 다음 메일러로 전환하며 순차적으로 분산 발송합니다. `failover` 방식이 *[고가용성(high availability)](https://en.wikipedia.org/wiki/High_availability)*을 추구한다면, `roundrobin` 방식은 *[로드 밸런싱(load balancing)](https://en.wikipedia.org/wiki/Load_balancing_(computing))*을 제공합니다.

<a name="generating-mailables"></a>
## 메일러블 생성 (Generating Mailables)

Laravel 애플리케이션에서는, 애플리케이션이 발송하는 각 유형의 이메일이 "메일러블(mailable)" 클래스 하나로 표현됩니다. 이 클래스들은 `app/Mail` 디렉토리에 저장됩니다. 이 디렉토리가 보이지 않더라도 걱정하지 마세요. `make:mail` Artisan 명령어로 메일러블 클래스를 생성하면 자동으로 생성됩니다.

```shell
php artisan make:mail OrderShipped
```

<a name="writing-mailables"></a>
## 메일러블 작성 (Writing Mailables)

메일러블 클래스를 생성했다면, 파일을 열어 내용을 살펴봅시다. 메일러블 클래스는 `envelope`, `content`, `attachments` 메서드에서 다양한 설정을 할 수 있습니다.

`envelope` 메서드는 메시지의 제목과 (필요에 따라) 받는 사람을 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 본문 생성을 위한 [Blade 템플릿](/docs/12.x/blade)을 지정하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 보낸 사람 설정

<a name="using-the-envelope"></a>
#### Envelope를 통한 설정

이메일의 보낸 사람, 즉 "from"을 어떻게 설정하는지 알아봅시다. 방법은 두 가지가 있습니다. 첫째, 메시지의 envelope에서 "from" 주소를 지정할 수 있습니다.

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

추가로 `replyTo` 주소를 지정할 수도 있습니다.

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
#### 전역 `from` 주소 사용

애플리케이션 전체에서 같은 "from" 주소를 사용할 경우, 매번 메일러블 클래스에 지정하는 것이 번거로울 수 있습니다. 이런 경우에는 `config/mail.php` 설정 파일에 전역 "from" 주소를 지정할 수 있습니다. 메일러블 클래스에서 별도 지정이 없다면 이 주소가 기본으로 사용됩니다.

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

또한, 전역 "reply_to" 주소도 `config/mail.php`에 설정할 수 있습니다.

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a name="configuring-the-view"></a>
### 뷰 설정

메일러블 클래스의 `content` 메서드 내에서 어떤 템플릿(view)을 사용할지 지정할 수 있습니다. 이메일마다 [Blade 템플릿](/docs/12.x/blade)으로 이메일 내용을 렌더링하므로, Blade 템플릿 엔진의 모든 기능을 자유롭게 활용할 수 있습니다.

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
> 이메일 템플릿을 보관하기 위해 `resources/views/mail` 디렉토리를 만들 수도 있지만, `resources/views` 디렉토리 내 어디에든 자유롭게 저장할 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 정의하고 싶다면, 메시지의 `Content` 정의 시 plain-text 템플릿을 명시할 수 있습니다. `view`와 마찬가지로, `text` 파라미터에는 이메일의 내용을 렌더링할 템플릿명을 입력합니다. HTML 및 plain-text 버전을 모두 지정할 수 있습니다.

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

더 명확히 구분하기 위해, `html` 파라미터를 `view` 파라미터의 별칭으로 사용할 수도 있습니다.

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a name="view-data"></a>
### 뷰 데이터

<a name="via-public-properties"></a>
#### public 속성을 통한 전달

이메일을 렌더링할 때 뷰(Blade 템플릿)에서 활용할 데이터를 전달하고 싶을 것입니다. 이를 위한 방법은 두 가지입니다. 첫째, 메일러블 클래스에서 정의한 public 속성은 자동으로 뷰에서 사용할 수 있습니다. 예를 들어, 생성자에서 데이터를 받아 public 속성에 할당하면 됩니다.

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

public 속성에 데이터가 할당되면, Blade 템플릿에서 아래와 같이 사용할 수 있습니다.

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a name="via-the-with-parameter"></a>
#### `with` 파라미터를 통한 전달

템플릿으로 전달하는 데이터의 포맷을 직접 조정하고 싶다면, `Content` 정의의 `with` 파라미터를 통해 데이터를 명시적으로 전달할 수 있습니다. 이 경우에도 생성자를 통해 데이터를 받아오지만, 데이터를 public이 아닌 protected 또는 private 속성에 저장하면 템플릿에 자동 노출되지 않습니다.

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

이렇게 `with` 파라미터로 데이터를 전달하면, Blade 템플릿에서 다음과 같이 접근할 수 있습니다.

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a name="attachments"></a>
### 첨부 파일

이메일에 첨부 파일을 추가하려면, 메시지의 `attachments` 메서드에서 반환하는 배열에 첨부 파일을 추가합니다. 먼저, `Attachment` 클래스의 `fromPath` 메서드로 파일 경로를 지정해 첨부할 수 있습니다.

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

첨부 파일에 표시 이름과 MIME 타입을 지정할 수도 있으며, 이를 위해 `as`와 `withMime` 메서드를 사용할 수 있습니다.

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
#### 파일 시스템에서 파일 첨부

파일을 [파일시스템 디스크](/docs/12.x/filesystem)에 저장해 두었다면, `fromStorage` 첨부 메서드로 이메일에 첨부할 수 있습니다.

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

이름과 MIME 타입도 같이 지정할 수 있습니다.

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

기본 디스크가 아닌 다른 스토리지 디스크를 지정해야 한다면 `fromStorageDisk` 메서드를 사용할 수 있습니다.

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
#### Raw 데이터 첨부

메모리에서 바로 생성한 PDF 등, 파일로 저장하지 않고도 첨부해야 할 때는 `fromData` 첨부 메서드를 사용할 수 있습니다. 이때, 클로저를 통해 raw 데이터 바이트와 첨부될 파일명을 전달해야 합니다.

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
### 인라인 첨부 파일

이메일에 인라인 이미지를 삽입하는 작업은 보통 번거롭지만, Laravel에서는 쉽게 이미지 첨부가 가능합니다. 이메일 템플릿 내부에서 `$message` 변수의 `embed` 메서드를 사용하면 이미지를 임베드할 수 있습니다. `$message` 변수는 모든 이메일 템플릿에 자동으로 제공되어 별도로 전달할 필요가 없습니다.

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> [!WARNING]
> `$message` 변수는 plain-text 템플릿에서는 사용할 수 없습니다. plain-text 메시지는 인라인 첨부를 지원하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### Raw 데이터로 인라인 이미지 임베드

이미 raw 형태의 이미지 데이터를 가지고 있다면, `$message` 변수의 `embedData` 메서드를 사용할 수 있습니다. 이때도 임베드할 파일명을 같이 전달해야 합니다.

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a name="attachable-objects"></a>
### Attachable 객체

문자열 경로로 파일을 첨부하는 방식이 간단하지만, 애플리케이션에서 첨부해야 하는 엔티티가 클래스(모델 객체 등)로 표현되는 경우도 많습니다. 예를 들어 사진(Photo) 모델이 존재하는 상황이라면, 모델 객체를 직접 첨부파일로 전달할 수 있으면 편리할 것입니다. Attachable 객체가 바로 이 역할을 합니다.

사용하려면, 첨부할 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하면 됩니다. 이 인터페이스는 `toMailAttachment` 메서드를 정의해야 하며, 여기서 `Illuminate\Mail\Attachment` 인스턴스를 반환해야 합니다.

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

이제 `attachments` 메서드에서 해당 객체를 배열로 반환하면 첨부가 됩니다.

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

당연히 첨부 데이터가 Amazon S3 등 원격 파일 스토리지에 저장되어 있을 수도 있습니다. Laravel에서는 애플리케이션의 [파일시스템 디스크](/docs/12.x/filesystem)에 저장된 데이터를 기반으로 첨부 인스턴스를 만들 수 있습니다.

```php
// 기본 디스크의 파일 첨부
return Attachment::fromStorage($this->path);

// 특정 디스크의 파일 첨부
return Attachment::fromStorageDisk('backblaze', $this->path);
```

메모리에 있는 데이터를 첨부 인스턴스로 만들고 싶다면 `fromData` 메서드에 클로저를 전달하면 됩니다. 클로저는 첨부 데이터를 반환해야 합니다.

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

첨부파일의 이름이나 MIME 타입을 커스터마이즈하려면 `as` 와 `withMime` 메서드를 활용하세요.

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a name="headers"></a>
### 헤더

추가적인 헤더를 아웃고잉(발송) 메시지에 붙여야 할 때가 있습니다. 예를 들어, 커스텀 `Message-Id`나 임의의 텍스트 헤더를 추가해야 할 수 있습니다.

이 기능은 메일러블에 `headers` 메서드를 정의하여 구현할 수 있습니다. 이 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 하며, 이 클래스는 `messageId`, `references`, `text` 파라미터를 받습니다. 필요한 항목만 전달하면 됩니다.

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
### 태그와 메타데이터

일부 외부 이메일 서비스(Mailgun, Postmark 등)는 메일 메시지에 "태그"나 "메타데이터"를 첨부하여 그룹화 및 추적을 지원합니다. 이런 태그 및 메타데이터는 `Envelope` 정의에서 지정할 수 있습니다.

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

Mailgun 드라이버를 사용할 경우 [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)에 대한 자료는 Mailgun 공식 문서에서 더 자세히 볼 수 있습니다. 마찬가지로, Postmark에서의 [태그](https://postmarkapp.com/blog/tags-support-for-smtp), [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 지원에 관한 문서도 참고하세요.

Amazon SES로 메일을 보낼 경우, `metadata` 메서드를 사용해 [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 메시지에 첨부할 수 있습니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 커스텀

Laravel의 메일 기능은 Symfony Mailer를 기반으로 제공합니다. Laravel에서는 이메일 전송 전에 Symfony Message 인스턴스에 대해 실행될 커스텀 콜백을 등록할 수 있어, 메시지를 더욱 상세하게 커스터마이즈할 수 있습니다. 이를 위해 `Envelope` 정의에서 `using` 파라미터를 사용하세요.

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

Markdown 메일러블 메시지는 [메일 알림](/docs/12.x/notifications#mail-notifications)의 미리 만들어진 템플릿 및 컴포넌트를 그대로 활용하는 장점이 있습니다. 메시지는 Markdown 문법으로 작성되며, Laravel이 보기 좋은 반응형 HTML 템플릿과 plain-text 버전을 자동으로 생성해 줍니다.

<a name="generating-markdown-mailables"></a>
### Markdown 메일러블 생성

Markdown 템플릿과 함께 메일러블을 생성하려면, `make:mail` Artisan 명령어에서 `--markdown` 옵션을 사용하세요.

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

그런 다음, 메일러블의 `content` 메서드 내에서 `view` 대신 `markdown` 파라미터를 사용해 Content를 정의합니다.

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
### Markdown 메시지 작성

Markdown 메일러블은 Blade 컴포넌트와 Markdown 문법을 조합해, Laravel의 사전 제작된 이메일 UI 컴포넌트를 손쉽게 사용할 수 있게 합니다.

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
> Markdown 이메일 작성 시 들여쓰기를 과도하게 하지 마세요. Markdown 표준에 따라, 들여쓴 콘텐츠는 코드 블록으로 처리됩니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬 버튼 링크를 렌더링합니다. `url`과 선택적 `color` 두 가지 인수를 받을 수 있으며, 지원하는 색상은 `primary`, `success`, `error`입니다. 메시지에 버튼 컴포넌트를 여러 개 추가할 수도 있습니다.

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 지정한 텍스트 블록을 메시지 내의 다른 영역보다 배경색이 약간 다른 패널로 감쌉니다. 이를 통해 특정 블록에 시각적 강조를 줄 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트는 Markdown 테이블을 HTML 테이블로 변환해서 렌더링합니다. 컴포넌트의 내용으로 Markdown 테이블을 그대로 작성하세요. 컬럼 정렬은 Markdown 표준 테이블 정렬 문법을 지원합니다.

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 커스터마이즈

Markdown 메일 컴포넌트를 애플리케이션에 가져와 원하는 대로 커스터마이즈할 수 있습니다. 컴포넌트는 `vendor:publish` Artisan 명령어로 `laravel-mail` 에셋 태그로 퍼블리시할 수 있습니다.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령을 실행하면, Markdown 메일 컴포넌트가 `resources/views/vendor/mail` 디렉토리에 복사됩니다. `mail` 디렉토리에는 각각 `html`과 `text` 디렉토리가 있으며, 각 템플릿 컴포넌트의 내용이 포함되어 있습니다. 이 컴포넌트들은 자유롭게 수정하여 사용할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 커스터마이즈

컴포넌트를 내보낸 후에는, `resources/views/vendor/mail/html/themes` 디렉토리에 생성된 `default.css` 파일을 수정해 스타일을 바꿀 수 있습니다. 이렇게 하면, 스타일이 자동으로 HTML 마크업에 인라인 CSS로 적용되어 반영됩니다.

Laravel의 Markdown 컴포넌트에 완전히 새로운 테마를 적용하려면 CSS 파일을 `html/themes` 디렉토리에 추가하고, `config/mail.php` 파일의 `theme` 옵션 값을 새 테마 이름으로 변경하면 됩니다.

특정 메일러블에만 별도 테마를 적용하려면, 메일러블 클래스의 `$theme` 속성에 사용할 테마 이름을 설정하면 됩니다.

<a name="sending-mail"></a>
## 메일 발송 (Sending Mail)

메일을 발송하려면, `Mail` [파사드](/docs/12.x/facades)의 `to` 메서드를 사용하세요. 이 메서드는 이메일 주소, 사용자 인스턴스, 사용자 컬렉션을 인수로 받을 수 있습니다. 객체나 객체의 컬렉션이 전달되면, 객체의 `email`과 `name` 속성을 알아서 추출하여 수신자로 지정합니다. 수신자를 지정한 후에는, 메일러블 클래스 인스턴스를 `send` 메서드에 전달하면 됩니다.

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

수신자("to")뿐 아니라 "cc", "bcc"도 각각의 메서드를 체이닝하여 지정할 수 있습니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a name="looping-over-recipients"></a>
#### 수신자 루프 처리

배열이나 여러 수신자 이메일 주소에 메일러블을 순차 발송해야 할 경우가 있습니다. 이때, 각 순회마다 이전 수신자에게도 추가적으로 메일이 발송될 수 있으니, 반드시 각 수신자마다 새로운 메일러블 인스턴스를 생성해야 합니다.

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러 지정 발송

기본적으로 Laravel은 `mail` 설정 파일의 `default` 메일러를 사용합니다. 하지만, `mailer` 메서드를 사용하면 특정 메일러 설정을 지정해 발송할 수 있습니다.

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 발송이 애플리케이션의 응답 속도에 영향을 미칠 수 있으므로, 많은 개발자들이 이메일을 백그라운드에서 큐로 발송하는 방식을 택합니다. Laravel에서는 [통합 큐 API](/docs/12.x/queues)를 활용해 이 작업이 매우 쉽습니다. 수신자 지정 후, `Mail` 파사드의 `queue` 메서드를 사용하면 자동으로 큐 작업이 생성되어 백그라운드 전송이 처리됩니다. 이 기능을 사용하려면 [큐 환경 설정](/docs/12.x/queues)을 먼저 마쳐야 합니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

<a name="delayed-message-queueing"></a>
#### 지연된 메시지 큐잉

큐에 등록된 이메일 발송을 지연시키고 싶다면, `later` 메서드를 사용할 수 있습니다. 이 메서드의 첫 번째 인수로는 메일을 언제 발송할지 나타내는 `DateTime` 인스턴스를 전달해야 합니다.

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->plus(minutes: 10), new OrderShipped($order));
```

<a name="pushing-to-specific-queues"></a>
#### 특정 큐로 전송하기

`make:mail` 명령어로 생성한 메일러블 클래스는 `Illuminate\Bus\Queueable` 트레이트를 기본적으로 사용하므로, 어느 인스턴스든 `onQueue`, `onConnection` 메서드를 호출해 큐명과 연결명을 지정할 수 있습니다.

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
#### 기본적으로 큐잉 처리

항상 큐로 발송되어야 하는 메일러블 클래스라면, 클래스에 `ShouldQueue` 인터페이스를 구현하세요. 이제 `send` 메서드로 발송하더라도 큐잉되어 발송됩니다.

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a name="queued-mailables-and-database-transactions"></a>
#### 큐잉된 메일러블과 데이터베이스 트랜잭션

큐잉된 메일러블이 데이터베이스 트랜잭션 내에서 디스패치되는 경우, 큐 작업이 트랜잭션 커밋보다 먼저 처리될 수 있습니다. 이 때문에, 트랜잭션 동안 변경한 모델이나 레코드가 데이터베이스에 반영되지 않았거나, 새로 생성된 레코드는 DB에 존재하지 않을 수 있어 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정 옵션이 `false`로 되어 있다면, 메일 메시지 전송 시 `afterCommit` 메서드를 호출해 모든 트랜잭션 커밋 이후 전송하도록 할 수 있습니다.

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

또는, 메일러블의 생성자에서 `afterCommit`을 호출합니다.

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
> 이 문제에 대한 자세한 대처 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-email-failures"></a>
#### 큐잉된 이메일 발송 실패

큐잉된 이메일이 실패할 경우, 해당 메일러블 클래스에 `failed` 메서드가 정의되어 있다면 자동으로 호출됩니다. 실패 원인으로 발생한 `Throwable` 인스턴스가 인수로 전달됩니다.

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

가끔 메일을 실제로 발송하지 않고 메일의 HTML 콘텐츠만 얻고 싶을 수 있습니다. 이 경우, 메일러블의 `render` 메서드를 호출하면 됩니다. 이 메서드는 평가된 HTML 콘텐츠를 문자열로 반환합니다.

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일러블 미리보기

메일러블의 템플릿을 디자인할 때, 실제 이메일로 발송하지 않고도 웹 브라우저에서 미리 볼 수 있다면 매우 편리합니다. 이런 이유로, Laravel에서는 라우트 클로저나 컨트롤러에서 메일러블 인스턴스를 직접 반환하면, 실제 이메일 주소로 전송하지 않아도 브라우저에서 디자인을 바로 확인할 수 있습니다.

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a name="localizing-mailables"></a>
## 메일러블 현지화 (Localizing Mailables)

Laravel은 요청의 현 로케일과 다른 로케일로 메일러블을 보낼 수 있도록 하며, 큐잉 시에도 이 로케일 정보를 기억합니다.

이를 위해, `Mail` 파사드는 원하는 언어를 지정하기 위한 `locale` 메서드를 제공합니다. 메일러블의 템플릿을 평가하는 동안만 해당 로케일로 변경되며, 완료 후 이전 로케일로 복원됩니다.

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일 적용

애플리케이션에서 각 사용자의 선호 로케일을 저장하는 경우가 있습니다. 모델에 `HasLocalePreference` 인터페이스를 구현하면 Laravel이 메일 전송 시 해당 로케일을 자동으로 사용하게 할 수 있습니다.

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

인터페이스를 구현하면, 별도로 `locale` 메서드를 호출하지 않아도 메일러블 및 알림 발송시 자동으로 사용자의 선호 로케일이 적용됩니다.

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a name="testing-mailables"></a>
## 테스트 (Testing)

<a name="testing-mailable-content"></a>
### 메일러블 콘텐츠 테스트

Laravel은 메일러블 구조를 살펴보는 여러 방법을 제공합니다. 또한, 메일러블에 기대하는 내용이 포함되어 있는지 편리하게 테스트하는 다양한 메서드도 지원합니다.

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

여기서 "HTML" 관련 assertion은 HTML 버전의 메일러블에 특정 문자열이 있는지, "text" 관련 assertion은 plain-text 버전에 특정 문자열이 있는지를 검사합니다.

<a name="testing-mailable-sending"></a>
### 메일러블 발송 테스트

메일러블의 내용을 검증하는 테스트와, 특정 메일러블이 특정 사용자에게 "발송"되었는지를 검증하는 테스트는 분리하는 것이 좋습니다. 실제로, 테스트 중인 코드와 무관한 메일 콘텐츠까지 검증할 필요는 없으므로, Laravel에서 특정 메일러블이 발송되었는지만 확인해도 충분합니다.

`Mail` 파사드의 `fake` 메서드를 호출하면 실제 메일 발송이 일어나지 않도록 막을 수 있습니다. 이후에, 실제로 어떤 메일러블이 어떤 데이터와 함께 발송 명령이 내려졌는지 다양하게 assertion 할 수 있습니다.

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

백그라운드로 큐잉해서 메일러블을 전송하는 경우에는, `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다.

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

발송, 큐잉된 전체 메일러블 개수는 `assertOutgoingCount` 메서드로 검증할 수 있습니다.

```php
Mail::assertOutgoingCount(3);
```

클로저를 `assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에 전달해, 특정 조건을 만족하는 메일러블이 적어도 하나 발송/큐잉되었는지 검사할 수도 있습니다.

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

assert 메서드에 전달되는 메일러블 인스턴스에서는 다음과 같이 편리한 검증용 메서드도 제공합니다.

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

첨부파일에 대한 유틸리티 메서드도 다양하게 사용할 수 있습니다.

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

메일이 발송되지 않았음을 검사하는 방법에는 `assertNotSent`와 `assertNotQueued` 두 가지가 있으며, 메일이 발송 **또는** 큐잉되지 않았는지도 아래처럼 판단할 수 있습니다.

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="mail-and-local-development"></a>
## 메일과 로컬 개발 환경 (Mail and Local Development)

이메일을 발송하는 애플리케이션을 개발할 때 실제 메일이 라이브 주소로 발송되는 것을 원하지 않을 수 있습니다. Laravel은 로컬 개발 중 실제 메일 발송을 "비활성화"할 수 있는 여러 방법을 제공합니다.

<a name="log-driver"></a>
#### 로그 드라이버

이메일을 실제로 발송하지 않고, 모든 이메일 메시지를 로그 파일에 기록하는 `log` 메일 드라이버를 사용할 수 있습니다. 이 드라이버는 주로 개발 환경에서 사용되며, 환경별 설정에 대한 자세한 내용은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

또는 [HELO](https://usehelo.com) 또는 [Mailtrap](https://mailtrap.io), 그리고 `smtp` 드라이버를 사용해 실제 발송 없이 "가상" 메일함으로 메시지를 보내고, 이메일 클라이언트에서 내용을 확인해볼 수 있습니다. 이 방법을 사용하면 최종 이메일이 어떻게 보일지 실제로 검사할 수 있습니다.

[Laravel Sail](/docs/12.x/sail)을 사용하는 경우, [Mailpit](https://github.com/axllent/mailpit)으로 메시지를 확인할 수 있습니다. Sail 실행 중에는 `http://localhost:8025`에서 Mailpit 인터페이스에 접속할 수 있습니다.

<a name="using-a-global-to-address"></a>
#### 전역 `to` 주소 사용

마지막으로, `Mail` 파사드의 `alwaysTo` 메서드를 사용해 모든 발송 메일을 지정된 주소로만 보내도록 할 수 있습니다. 일반적으로, 이 메서드는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 호출하면 좋습니다.

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

`alwaysTo` 메서드를 사용할 때는, 메일에 지정된 추가 "cc"나 "bcc" 주소가 모두 제거됩니다.

<a name="events"></a>
## 이벤트 (Events)

Laravel은 메일 발송 시 두 가지 이벤트를 발생시킵니다. 메시지 발송 전에 `MessageSending` 이벤트가, 발송 후에는 `MessageSent` 이벤트가 발생합니다. 이 이벤트들은 *발송* 단계에서만 발생하며 *큐잉* 단계는 아닙니다. 애플리케이션에서 [이벤트 리스너](/docs/12.x/events)를 만들어 활용할 수 있습니다.

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

Laravel은 다양한 메일 전송 방식을 내장하지만, 필요하다면 직접 원하는 서비스를 위한 커스텀 전송 방식을 작성할 수 있습니다. 우선, `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 상속받은 클래스를 정의하고, `doSend` 및 `__toString` 메서드를 구현해야 합니다.

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

커스텀 트랜스포트를 정의했다면, `Mail` 파사드의 `extend` 메서드로 등록할 수 있습니다. 일반적으로 이 작업은 `AppServiceProvider`의 `boot` 메서드에서 이루어집니다. `extend`에 전달하는 클로저에는 `config/mail.php`에 정의된 해당 메일러의 설정 배열이 `$config` 인수로 전달됩니다.

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

커스텀 트랜스포트를 정의 및 등록했다면, 이제 `config/mail.php` 파일의 메일러 정의에서 새 전송 방식을 지정할 수 있습니다.

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송 방식

Laravel은 Mailgun, Postmark처럼 이미 일부 Symfony에서 관리하는 메일 전송 방식을 지원하지만, 추가로 Symfony에서 관리하는 기타 전송 방식을 직접 추가할 수도 있습니다. Composer로 해당 Symfony 메일러를 설치하고, Laravel에 등록하면 됩니다. 예를 들어, "Brevo"(이전 Sendinblue) Symfony 메일러를 설치하고 등록하려면 다음과 같습니다.

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Brevo 메일러 패키지를 설치한 후, 애플리케이션의 `services` 설정 파일에 Brevo API 자격 증명을 추가하세요.

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

그리고, 서비스 프로바이더의 `boot` 메서드에서 `Mail` 파사드의 `extend` 메서드로 트랜스포트를 등록합니다.

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

등록이 완료되면, `config/mail.php` 설정 파일 내에서 새 전송 방식을 사용하는 메일러를 만들 수 있습니다.

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
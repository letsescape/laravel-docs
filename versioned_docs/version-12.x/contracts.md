# 컨트랙트 (Contracts)

- [소개](#introduction)
    - [컨트랙트와 파사드 비교](#contracts-vs-facades)
- [컨트랙트를 언제 사용하나요?](#when-to-use-contracts)
- [컨트랙트 사용 방법](#how-to-use-contracts)
- [컨트랙트 참고 자료](#contract-reference)

<a name="introduction"></a>
## 소개

Laravel의 "컨트랙트"는 프레임워크가 제공하는 핵심 서비스를 정의하는 인터페이스 집합입니다. 예를 들어, `Illuminate\Contracts\Queue\Queue` 컨트랙트는 작업을 큐잉하는 데 필요한 메서드를 정의하고, `Illuminate\Contracts\Mail\Mailer` 컨트랙트는 이메일을 전송하는 데 필요한 메서드를 정의합니다.

각 컨트랙트에는 프레임워크에서 제공하는 대응하는 구현체가 있습니다. 예를 들어, Laravel은 다양한 드라이버를 지원하는 큐 구현체와 [Symfony Mailer](https://symfony.com/doc/current/mailer.html)를 기반으로 작동하는 메일러 구현체를 제공합니다.

모든 Laravel 컨트랙트는 [별도의 GitHub 저장소](https://github.com/illuminate/contracts)에서 관리됩니다. 이 저장소는 모든 사용 가능한 컨트랙트의 빠른 참고 자료를 제공함과 동시에, Laravel 서비스와 상호작용하는 패키지를 만들 때 사용할 수 있는 단일 독립 패키지를 제공합니다.

<a name="contracts-vs-facades"></a>
### 컨트랙트와 파사드 비교

Laravel의 [파사드](/docs/12.x/facades)와 헬퍼 함수는 서비스 컨테이너에서 명시적으로 컨트랙트를 타입-힌트 하거나 해석할 필요 없이 Laravel 서비스를 간편하게 사용할 수 있는 방법입니다. 대부분의 경우, 각 파사드는 동일한 기능을 제공하는 컨트랙트를 갖고 있습니다.

파사드는 클래스 생성자에서 별도로 주입받을 필요가 없지만, 컨트랙트는 클래스의 명시적인 의존성을 정의할 수 있도록 해줍니다. 일부 개발자는 의존성을 명확히 정의하는 방식을 선호하여 컨트랙트를 더 선호하는 반면, 다른 개발자는 파사드의 간편함을 더 선호합니다. **일반적으로 대부분의 애플리케이션은 개발 과정에서 파사드를 문제 없이 사용할 수 있습니다.**

<a name="when-to-use-contracts"></a>
## 컨트랙트를 언제 사용하나요?

컨트랙트를 사용할지, 파사드를 사용할지 결정하는 것은 개인의 취향과 개발 팀의 상황에 달려 있습니다. 컨트랙트와 파사드는 모두 견고하고 테스트하기 좋은 Laravel 애플리케이션을 만드는 데 사용할 수 있습니다. 두 방식은 상호 배타적이지 않습니다. 애플리케이션의 일부는 파사드를 사용하고, 다른 일부는 컨트랙트를 의존할 수 있습니다. 클래스의 책임이 명확히 분리되어 있다면, 컨트랙트와 파사드를 사용하는 것 간에 실제적으로 큰 차이를 느끼기 어렵습니다.

일반적으로 대다수 애플리케이션은 개발하는 동안 파사드를 문제 없이 사용할 수 있습니다. 만약 여러 PHP 프레임워크와 통합하는 패키지를 개발한다면, `illuminate/contracts` 패키지를 사용하여 Laravel 서비스와의 통합을 정의하는 것이 좋습니다. 이렇게 하면 패키지의 `composer.json`에 Laravel의 구체적인 구현체를 꼭 명시하지 않아도 됩니다.

<a name="how-to-use-contracts"></a>
## 컨트랙트 사용 방법

그렇다면 컨트랙트의 구현체를 어떻게 획득할 수 있을까요? 사실 매우 간단합니다.

Laravel에서는 컨트롤러, 이벤트 리스너, 미들웨어, 큐 작업, 라우트 클로저 등 다양한 유형의 클래스가 [서비스 컨테이너](/docs/12.x/container)를 통해 해석(resolved)됩니다. 따라서 컨트랙트 구현체를 얻으려면, 해당 클래스 생성자의 인수 타입 힌트로 인터페이스를 지정하면 됩니다.

예를 들어, 다음의 이벤트 리스너를 살펴보세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderWasPlaced;
use App\Models\User;
use Illuminate\Contracts\Redis\Factory;

class CacheOrderInformation
{
    /**
     * 이벤트 리스너 생성자.
     */
    public function __construct(
        protected Factory $redis,
    ) {}

    /**
     * 이벤트 처리 메서드.
     */
    public function handle(OrderWasPlaced $event): void
    {
        // ...
    }
}
```

이 이벤트 리스너가 해석될 때, 서비스 컨테이너는 클래스 생성자의 타입 힌트를 읽어 알맞은 값을 자동으로 주입합니다. 서비스 컨테이너에 등록하는 방법에 대해 더 알고 싶다면, [관련 문서](/docs/12.x/container)를 참고하세요.

<a name="contract-reference"></a>
## 컨트랙트 참고 자료

아래 표는 Laravel의 모든 컨트랙트와 대응하는 파사드를 빠르게 참고할 수 있도록 정리한 것입니다:

<div class="overflow-auto">

| 컨트랙트 | 연관된 파사드 |
| --- | --- |
| [Illuminate\Contracts\Auth\Access\Authorizable](https://github.com/illuminate/contracts/blob/12.x/Auth/Access/Authorizable.php) | &nbsp; |
| [Illuminate\Contracts\Auth\Access\Gate](https://github.com/illuminate/contracts/blob/12.x/Auth/Access/Gate.php) | `Gate` |
| [Illuminate\Contracts\Auth\Authenticatable](https://github.com/illuminate/contracts/blob/12.x/Auth/Authenticatable.php) | &nbsp; |
| [Illuminate\Contracts\Auth\CanResetPassword](https://github.com/illuminate/contracts/blob/12.x/Auth/CanResetPassword.php) | &nbsp; |
| [Illuminate\Contracts\Auth\Factory](https://github.com/illuminate/contracts/blob/12.x/Auth/Factory.php) | `Auth` |
| [Illuminate\Contracts\Auth\Guard](https://github.com/illuminate/contracts/blob/12.x/Auth/Guard.php) | `Auth::guard()` |
| [Illuminate\Contracts\Auth\PasswordBroker](https://github.com/illuminate/contracts/blob/12.x/Auth/PasswordBroker.php) | `Password::broker()` |
| [Illuminate\Contracts\Auth\PasswordBrokerFactory](https://github.com/illuminate/contracts/blob/12.x/Auth/PasswordBrokerFactory.php) | `Password` |
| [Illuminate\Contracts\Auth\StatefulGuard](https://github.com/illuminate/contracts/blob/12.x/Auth/StatefulGuard.php) | &nbsp; |
| [Illuminate\Contracts\Auth\SupportsBasicAuth](https://github.com/illuminate/contracts/blob/12.x/Auth/SupportsBasicAuth.php) | &nbsp; |
| [Illuminate\Contracts\Auth\UserProvider](https://github.com/illuminate/contracts/blob/12.x/Auth/UserProvider.php) | &nbsp; |
| [Illuminate\Contracts\Broadcasting\Broadcaster](https://github.com/illuminate/contracts/blob/12.x/Broadcasting/Broadcaster.php) | `Broadcast::connection()` |
| [Illuminate\Contracts\Broadcasting\Factory](https://github.com/illuminate/contracts/blob/12.x/Broadcasting/Factory.php) | `Broadcast` |
| [Illuminate\Contracts\Broadcasting\ShouldBroadcast](https://github.com/illuminate/contracts/blob/12.x/Broadcasting/ShouldBroadcast.php) | &nbsp; |
| [Illuminate\Contracts\Broadcasting\ShouldBroadcastNow](https://github.com/illuminate/contracts/blob/12.x/Broadcasting/ShouldBroadcastNow.php) | &nbsp; |
| [Illuminate\Contracts\Bus\Dispatcher](https://github.com/illuminate/contracts/blob/12.x/Bus/Dispatcher.php) | `Bus` |
| [Illuminate\Contracts\Bus\QueueingDispatcher](https://github.com/illuminate/contracts/blob/12.x/Bus/QueueingDispatcher.php) | `Bus::dispatchToQueue()` |
| [Illuminate\Contracts\Cache\Factory](https://github.com/illuminate/contracts/blob/12.x/Cache/Factory.php) | `Cache` |
| [Illuminate\Contracts\Cache\Lock](https://github.com/illuminate/contracts/blob/12.x/Cache/Lock.php) | &nbsp; |
| [Illuminate\Contracts\Cache\LockProvider](https://github.com/illuminate/contracts/blob/12.x/Cache/LockProvider.php) | &nbsp; |
| [Illuminate\Contracts\Cache\Repository](https://github.com/illuminate/contracts/blob/12.x/Cache/Repository.php) | `Cache::driver()` |
| [Illuminate\Contracts\Cache\Store](https://github.com/illuminate/contracts/blob/12.x/Cache/Store.php) | &nbsp; |
| [Illuminate\Contracts\Config\Repository](https://github.com/illuminate/contracts/blob/12.x/Config/Repository.php) | `Config` |
| [Illuminate\Contracts\Console\Application](https://github.com/illuminate/contracts/blob/12.x/Console/Application.php) | &nbsp; |
| [Illuminate\Contracts\Console\Kernel](https://github.com/illuminate/contracts/blob/12.x/Console/Kernel.php) | `Artisan` |
| [Illuminate\Contracts\Container\Container](https://github.com/illuminate/contracts/blob/12.x/Container/Container.php) | `App` |
| [Illuminate\Contracts\Cookie\Factory](https://github.com/illuminate/contracts/blob/12.x/Cookie/Factory.php) | `Cookie` |
| [Illuminate\Contracts\Cookie\QueueingFactory](https://github.com/illuminate/contracts/blob/12.x/Cookie/QueueingFactory.php) | `Cookie::queue()` |
| [Illuminate\Contracts\Database\ModelIdentifier](https://github.com/illuminate/contracts/blob/12.x/Database/ModelIdentifier.php) | &nbsp; |
| [Illuminate\Contracts\Debug\ExceptionHandler](https://github.com/illuminate/contracts/blob/12.x/Debug/ExceptionHandler.php) | &nbsp; |
| [Illuminate\Contracts\Encryption\Encrypter](https://github.com/illuminate/contracts/blob/12.x/Encryption/Encrypter.php) | `Crypt` |
| [Illuminate\Contracts\Events\Dispatcher](https://github.com/illuminate/contracts/blob/12.x/Events/Dispatcher.php) | `Event` |
| [Illuminate\Contracts\Filesystem\Cloud](https://github.com/illuminate/contracts/blob/12.x/Filesystem/Cloud.php) | `Storage::cloud()` |
| [Illuminate\Contracts\Filesystem\Factory](https://github.com/illuminate/contracts/blob/12.x/Filesystem/Factory.php) | `Storage` |
| [Illuminate\Contracts\Filesystem\Filesystem](https://github.com/illuminate/contracts/blob/12.x/Filesystem/Filesystem.php) | `Storage::disk()` |
| [Illuminate\Contracts\Foundation\Application](https://github.com/illuminate/contracts/blob/12.x/Foundation/Application.php) | `App` |
| [Illuminate\Contracts\Hashing\Hasher](https://github.com/illuminate/contracts/blob/12.x/Hashing/Hasher.php) | `Hash` |
| [Illuminate\Contracts\Http\Kernel](https://github.com/illuminate/contracts/blob/12.x/Http/Kernel.php) | &nbsp; |
| [Illuminate\Contracts\Mail\Mailable](https://github.com/illuminate/contracts/blob/12.x/Mail/Mailable.php) | &nbsp; |
| [Illuminate\Contracts\Mail\Mailer](https://github.com/illuminate/contracts/blob/12.x/Mail/Mailer.php) | `Mail` |
| [Illuminate\Contracts\Mail\MailQueue](https://github.com/illuminate/contracts/blob/12.x/Mail/MailQueue.php) | `Mail::queue()` |
| [Illuminate\Contracts\Notifications\Dispatcher](https://github.com/illuminate/contracts/blob/12.x/Notifications/Dispatcher.php) | `Notification`|
| [Illuminate\Contracts\Notifications\Factory](https://github.com/illuminate/contracts/blob/12.x/Notifications/Factory.php) | `Notification` |
| [Illuminate\Contracts\Pagination\LengthAwarePaginator](https://github.com/illuminate/contracts/blob/12.x/Pagination/LengthAwarePaginator.php) | &nbsp; |
| [Illuminate\Contracts\Pagination\Paginator](https://github.com/illuminate/contracts/blob/12.x/Pagination/Paginator.php) | &nbsp; |
| [Illuminate\Contracts\Pipeline\Hub](https://github.com/illuminate/contracts/blob/12.x/Pipeline/Hub.php) | &nbsp; |
| [Illuminate\Contracts\Pipeline\Pipeline](https://github.com/illuminate/contracts/blob/12.x/Pipeline/Pipeline.php) | `Pipeline` |
| [Illuminate\Contracts\Queue\EntityResolver](https://github.com/illuminate/contracts/blob/12.x/Queue/EntityResolver.php) | &nbsp; |
| [Illuminate\Contracts\Queue\Factory](https://github.com/illuminate/contracts/blob/12.x/Queue/Factory.php) | `Queue` |
| [Illuminate\Contracts\Queue\Job](https://github.com/illuminate/contracts/blob/12.x/Queue/Job.php) | &nbsp; |
| [Illuminate\Contracts\Queue\Monitor](https://github.com/illuminate/contracts/blob/12.x/Queue/Monitor.php) | `Queue` |
| [Illuminate\Contracts\Queue\Queue](https://github.com/illuminate/contracts/blob/12.x/Queue/Queue.php) | `Queue::connection()` |
| [Illuminate\Contracts\Queue\QueueableCollection](https://github.com/illuminate/contracts/blob/12.x/Queue/QueueableCollection.php) | &nbsp; |
| [Illuminate\Contracts\Queue\QueueableEntity](https://github.com/illuminate/contracts/blob/12.x/Queue/QueueableEntity.php) | &nbsp; |
| [Illuminate\Contracts\Queue\ShouldQueue](https://github.com/illuminate/contracts/blob/12.x/Queue/ShouldQueue.php) | &nbsp; |
| [Illuminate\Contracts\Redis\Factory](https://github.com/illuminate/contracts/blob/12.x/Redis/Factory.php) | `Redis` |
| [Illuminate\Contracts\Routing\BindingRegistrar](https://github.com/illuminate/contracts/blob/12.x/Routing/BindingRegistrar.php) | `Route` |
| [Illuminate\Contracts\Routing\Registrar](https://github.com/illuminate/contracts/blob/12.x/Routing/Registrar.php) | `Route` |
| [Illuminate\Contracts\Routing\ResponseFactory](https://github.com/illuminate/contracts/blob/12.x/Routing/ResponseFactory.php) | `Response` |
| [Illuminate\Contracts\Routing\UrlGenerator](https://github.com/illuminate/contracts/blob/12.x/Routing/UrlGenerator.php) | `URL` |
| [Illuminate\Contracts\Routing\UrlRoutable](https://github.com/illuminate/contracts/blob/12.x/Routing/UrlRoutable.php) | &nbsp; |
| [Illuminate\Contracts\Session\Session](https://github.com/illuminate/contracts/blob/12.x/Session/Session.php) | `Session::driver()` |
| [Illuminate\Contracts\Support\Arrayable](https://github.com/illuminate/contracts/blob/12.x/Support/Arrayable.php) | &nbsp; |
| [Illuminate\Contracts\Support\Htmlable](https://github.com/illuminate/contracts/blob/12.x/Support/Htmlable.php) | &nbsp; |
| [Illuminate\Contracts\Support\Jsonable](https://github.com/illuminate/contracts/blob/12.x/Support/Jsonable.php) | &nbsp; |
| [Illuminate\Contracts\Support\MessageBag](https://github.com/illuminate/contracts/blob/12.x/Support/MessageBag.php) | &nbsp; |
| [Illuminate\Contracts\Support\MessageProvider](https://github.com/illuminate/contracts/blob/12.x/Support/MessageProvider.php) | &nbsp; |
| [Illuminate\Contracts\Support\Renderable](https://github.com/illuminate/contracts/blob/12.x/Support/Renderable.php) | &nbsp; |
| [Illuminate\Contracts\Support\Responsable](https://github.com/illuminate/contracts/blob/12.x/Support/Responsable.php) | &nbsp; |
| [Illuminate\Contracts\Translation\Loader](https://github.com/illuminate/contracts/blob/12.x/Translation/Loader.php) | &nbsp; |
| [Illuminate\Contracts\Translation\Translator](https://github.com/illuminate/contracts/blob/12.x/Translation/Translator.php) | `Lang` |
| [Illuminate\Contracts\Validation\Factory](https://github.com/illuminate/contracts/blob/12.x/Validation/Factory.php) | `Validator` |
| [Illuminate\Contracts\Validation\ValidatesWhenResolved](https://github.com/illuminate/contracts/blob/12.x/Validation/ValidatesWhenResolved.php) | &nbsp; |
| [Illuminate\Contracts\Validation\ValidationRule](https://github.com/illuminate/contracts/blob/12.x/Validation/ValidationRule.php) | &nbsp; |
| [Illuminate\Contracts\Validation\Validator](https://github.com/illuminate/contracts/blob/12.x/Validation/Validator.php) | `Validator::make()` |
| [Illuminate\Contracts\View\Engine](https://github.com/illuminate/contracts/blob/12.x/View/Engine.php) | &nbsp; |
| [Illuminate\Contracts\View\Factory](https://github.com/illuminate/contracts/blob/12.x/View/Factory.php) | `View` |
| [Illuminate\Contracts\View\View](https://github.com/illuminate/contracts/blob/12.x/View/View.php) | `View::make()` |

</div>
<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 13](#laravel-13)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~Q1), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel과 그 밖의 first-party 패키지는 [Semantic Versioning](https://semver.org)을 따릅니다. 주요 프레임워크 릴리스는 매년 한 번씩(~1분기) 출시되며, 마이너 및 패치 릴리스는 매주 출시될 수도 있습니다. 마이너 및 패치 릴리스에는 **절대** 호환성을 깨는 변경 사항이 포함되어서는 안 됩니다.

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^13.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
애플리케이션이나 패키지에서 Laravel 프레임워크 또는 그 구성 요소를 참조할 때는 항상 `^13.0`과 같은 버전 제약을 사용해야 합니다. Laravel의 주요 릴리스에는 호환성을 깨는 변경 사항이 포함되기 때문입니다. 하지만 새로운 주요 릴리스로 하루 이내에 업데이트할 수 있도록 항상 노력하고 있습니다.

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- [Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 지침에 포함되지 않습니다. Laravel 코드베이스를 개선하기 위해 필요할 경우 함수 인수 이름을 변경할 수 있습니다. 따라서 Laravel 메서드를 호출할 때 명명된 인수를 사용할 때는 매개변수 이름이 향후 변경될 수 있음을 이해하고 신중하게 사용해야 합니다.

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/13.x/database#introduction). -->
모든 Laravel 릴리스에는 18개월 동안 버그 수정이 제공되며, 2년 동안 보안 수정이 제공됩니다. 그 밖의 모든 추가 라이브러리는 최신 주요 릴리스에만 버그 수정이 제공됩니다. 또한 [supported by Laravel](/docs/13.x/database#introduction) 데이터베이스 버전도 확인하시기 바랍니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 버전 | PHP (*) | 출시일 | 버그 수정 제공 기한 | 보안 수정 제공 기한 |
| ------- |-----------| ------------------- | ------------------- | -------------------- |
| 10      | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11      | 8.2 - 8.4 | 2024년 3월 12일 | 2025년 9월 3일 | 2026년 3월 12일 |
| 12      | 8.2 - 8.5 | 2025년 2월 24일 | 2026년 8월 13일 | 2027년 2월 24일 |
| 13      | 8.3 - 8.5 | 2026년 3월 17일 | 2027년 3분기 | 2028년 3월 17일 |

<!-- </div> -->
</div>

<!--
<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>
-->
<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>지원 종료</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>보안 수정만 제공</div>
    </div>
</div>

<!-- (*) Supported PHP versions -->
(*) 지원되는 PHP 버전

<a name="laravel-13"></a>
<!-- ## Laravel 13 -->
## Laravel 13

<!-- Laravel 13 continues Laravel's annual release cadence with a focus on AI-native workflows, stronger defaults, and more expressive developer APIs. This release includes first-party AI primitives, JSON:API resources, semantic / vector search capabilities, and incremental improvements across queues, cache, and security. -->
Laravel 13은 AI-native 워크플로, 더 강력한 기본값, 더 표현력 있는 개발자 API에 중점을 두며 Laravel의 연간 릴리스 주기를 이어갑니다. 이 릴리스에는 first-party AI 기본 기능, JSON:API 리소스, 시맨틱 / 벡터 검색 기능, 큐, 캐시, 보안 전반의 점진적인 개선 사항이 포함됩니다.

<a name="minimal-breaking-changes"></a>
<!-- ### Minimal Breaking Changes -->
### Minimal Breaking Changes

<!-- Much of our focus during this release cycle has been minimizing breaking changes. Instead, we have dedicated ourselves to shipping continuous quality-of-life improvements throughout the year that do not break existing applications. -->
이번 릴리스 주기 동안 주요 초점은 호환성을 깨는 변경 사항을 최소화하는 것이었습니다. 대신 기존 애플리케이션을 깨뜨리지 않는 지속적인 사용성 개선을 한 해 동안 제공하는 데 집중했습니다.

<!-- Therefore, the Laravel 13 release is a relatively minor upgrade in terms of effort, while still delivering substantial new capabilities. In light of this, most Laravel applications may upgrade to Laravel 13 without changing much application code. -->
따라서 Laravel 13 릴리스는 업그레이드에 필요한 노력 측면에서는 비교적 작은 업그레이드이지만, 동시에 상당한 새 기능을 제공합니다. 이러한 점을 고려하면 대부분의 Laravel 애플리케이션은 애플리케이션 코드를 많이 변경하지 않고도 Laravel 13으로 업그레이드할 수 있습니다.

<a name="php-8"></a>
<!-- ### PHP 8.3 -->
### PHP 8.3

<!-- Laravel 13.x requires a minimum PHP version of 8.3. -->
Laravel 13.x에는 최소 PHP 버전 8.3이 필요합니다.

<a name="ai-sdk"></a>
<!-- ### Laravel AI SDK -->
### Laravel AI SDK

<!-- Laravel 13 introduces the first-party [Laravel AI SDK](https://laravel.com/ai), providing a unified API for text generation, tool-calling agents, embeddings, audio, images, and vector-store integrations. -->
Laravel 13은 first-party [Laravel AI SDK](https://laravel.com/ai)를 도입합니다. 이 SDK는 텍스트 생성, 도구 호출 에이전트, 임베딩, 오디오, 이미지, vector-store 통합을 위한 통합 API를 제공합니다.

<!-- With the AI SDK, you can build provider-agnostic AI features while keeping a consistent, Laravel-native developer experience. -->
AI SDK를 사용하면 일관된 Laravel-native 개발자 경험을 유지하면서, 특정 제공자에 종속되지 않는 AI 기능을 만들 수 있습니다.

<!-- For example, a basic agent can be prompted with a single call: -->
예를 들어, 기본 에이전트는 한 번의 호출로 프롬프트를 전달할 수 있습니다.

```php
use App\Ai\Agents\SalesCoach;

$response = SalesCoach::make()->prompt('Analyze this sales transcript...');

return (string) $response;
```

<!-- The Laravel AI SDK can also generate images, audio, and embeddings: -->
Laravel AI SDK는 이미지, 오디오, 임베딩도 생성할 수 있습니다.

<!-- For visual generation use cases, the SDK offers a clean API for creating images from plain-language prompts: -->
시각적 생성 사용 사례를 위해 SDK는 자연어 프롬프트로 이미지를 생성하는 깔끔한 API를 제공합니다.

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

<!-- For voice experiences, you can synthesize natural-sounding audio from text for assistants, narrations, and accessibility features: -->
음성 경험을 위해서는 어시스턴트, 내레이션, 접근성 기능에 사용할 자연스러운 오디오를 텍스트에서 합성할 수 있습니다.

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

<!-- And for semantic search and retrieval workflows, you can generate embeddings directly from strings: -->
그리고 시맨틱 검색과 검색 기반 워크플로를 위해 문자열에서 직접 임베딩을 생성할 수 있습니다.

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<a name="json-api"></a>
<!-- ### JSON:API Resources -->
### JSON:API Resources

<!-- Laravel now includes first-party [JSON:API resources](/docs/13.x/eloquent-resources#jsonapi-resources), making it straightforward to return responses compliant with the JSON:API specification. -->
Laravel은 이제 first-party [JSON:API resources](/docs/13.x/eloquent-resources#jsonapi-resources)를 포함하여, JSON:API 명세를 준수하는 응답을 간단하게 반환할 수 있도록 합니다.

<!-- JSON:API resources handle resource object serialization, relationship inclusion, sparse fieldsets, links, and JSON:API-compliant response headers. -->
JSON:API 리소스는 리소스 객체 직렬화, 연관관계 포함, 희소 필드셋, 링크, JSON:API 호환 응답 헤더를 처리합니다.

<a name="request-forgery-protection"></a>
<!-- ### Request Forgery Protection -->
### Request Forgery Protection

<!-- For security, Laravel's [request forgery protection](/docs/13.x/csrf#preventing-csrf-requests) middleware has been enhanced and formalized as `PreventRequestForgery`, adding origin-aware request verification while preserving compatibility with token-based CSRF protection. -->
보안을 위해 Laravel의 [request forgery protection](/docs/13.x/csrf#preventing-csrf-requests) Middleware가 개선되고 `PreventRequestForgery`로 공식화되었습니다. 이를 통해 토큰 기반 CSRF 보호와의 호환성을 유지하면서, origin을 인식하는 요청 검증이 추가됩니다.

<a name="queue-routing"></a>
<!-- ### Queue Routing -->
### Queue Routing

<!-- Laravel 13 adds [queue routing by class](/docs/13.x/queues#queue-routing) via `Queue::route(...)`, allowing you to define default queue / connection routing rules for specific jobs in a central place: -->
Laravel 13은 `Queue::route(...)`를 통해 [queue routing by class](/docs/13.x/queues#queue-routing)을 추가합니다. 이를 사용하면 특정 job에 대한 기본 큐 / 연결 라우팅 규칙을 중앙에서 정의할 수 있습니다.

```php
Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
```

<a name="php-attributes"></a>
<!-- ### Expanded PHP Attributes -->
### Expanded PHP Attributes

<!-- Laravel 13 continues to expand first-party PHP attribute support across the framework, making common configuration and behavioral concerns more declarative and colocated with your classes and methods. -->
Laravel 13은 프레임워크 전반에서 first-party PHP attribute 지원을 계속 확장합니다. 이를 통해 일반적인 설정과 동작 관련 관심사를 더 선언적으로 표현하고, 클래스와 메서드 가까이에 함께 배치할 수 있습니다.

<!-- Notable additions include controller and authorization attributes like [`#[Middleware]`](/docs/13.x/controllers#controller-middleware) and [`#[Authorize]`](/docs/13.x/controllers#authorization-attributes), as well as queue-oriented job controls like [`#[Tries]`](/docs/13.x/queues#max-job-attempts-and-timeout), [`#[Backoff]`](/docs/13.x/queues#dealing-with-failed-jobs), [`#[Timeout]`](/docs/13.x/queues#max-job-attempts-and-timeout), and [`#[FailOnTimeout]`](/docs/13.x/queues#failing-on-timeout). -->
주요 추가 사항으로는 [`#[Middleware]`](/docs/13.x/controllers#controller-middleware), [`#[Authorize]`](/docs/13.x/controllers#authorization-attributes)와 같은 컨트롤러 및 인가 attribute가 있으며, [`#[Tries]`](/docs/13.x/queues#max-job-attempts-and-timeout), [`#[Backoff]`](/docs/13.x/queues#dealing-with-failed-jobs), [`#[Timeout]`](/docs/13.x/queues#max-job-attempts-and-timeout), [`#[FailOnTimeout]`](/docs/13.x/queues#failing-on-timeout)와 같은 큐 중심 job 제어 기능도 포함됩니다.

<!-- For example, controller middleware and policy checks can now be declared directly on classes and methods: -->
예를 들어, 컨트롤러 Middleware와 policy 검사를 이제 클래스와 메서드에 직접 선언할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Post;
use Illuminate\Routing\Attributes\Controllers\Authorize;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class CommentController
{
    #[Middleware('subscribed')]
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post)
    {
        // ...
    }
}
```

<!-- Additional attributes have also been introduced across Eloquent, events, notifications, validation, testing, and resource serialization APIs, giving you a consistent attribute-first option in more areas of the framework. -->
Eloquent, 이벤트, 알림, 유효성 검증, 테스트, 리소스 직렬화 API 전반에도 추가 attribute가 도입되어, 프레임워크의 더 많은 영역에서 일관된 attribute-first 옵션을 사용할 수 있습니다.

<a name="cache-touch"></a>
<!-- ### Cache TTL Extension -->
### Cache TTL Extension

<!-- Laravel now includes [`Cache::touch(...)`](/docs/13.x/cache), which lets you extend an existing cache item's TTL without retrieving and re-storing its value. -->
Laravel에는 이제 [`Cache::touch(...)`](/docs/13.x/cache)가 포함됩니다. 이를 사용하면 기존 캐시 항목의 값을 가져와 다시 저장하지 않고도 해당 항목의 TTL을 연장할 수 있습니다.

<a name="semantic-search"></a>
<!-- ### Semantic / Vector Search -->
### Semantic / Vector Search

<!-- Laravel 13 deepens its semantic search story with native vector query support, embedding workflows, and related APIs documented across [search](/docs/13.x/search#semantic-vector-search), [queries](/docs/13.x/queries#vector-similarity-clauses), and the [AI SDK](/docs/13.x/ai-sdk#embeddings). -->
Laravel 13은 네이티브 벡터 쿼리 지원, 임베딩 워크플로, 그리고 [search](/docs/13.x/search#semantic-vector-search), [queries](/docs/13.x/queries#vector-similarity-clauses), [AI SDK](/docs/13.x/ai-sdk#embeddings)에 걸쳐 문서화된 관련 API를 통해 시맨틱 검색 기능을 더욱 강화합니다.

<!-- These features make it straightforward to build AI-powered search experiences using PostgreSQL + `pgvector`, including similarity search against embeddings generated directly from strings. -->
이러한 기능을 사용하면 문자열에서 직접 생성한 임베딩을 대상으로 유사도 검색을 수행하는 것을 포함하여, PostgreSQL + `pgvector`를 활용한 AI 기반 검색 경험을 간단하게 구축할 수 있습니다.

<!-- For example, you may run semantic similarity searches directly from the query builder: -->
예를 들어, 쿼리 빌더에서 직접 시맨틱 유사도 검색을 실행할 수 있습니다.

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

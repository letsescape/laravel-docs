# 릴리즈 노트 (Release Notes)

- [버전 관리 정책](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 13](#laravel-13)

<a name="versioning-scheme"></a>
## 버전 관리 정책 (Versioning Scheme)

Laravel과 그 외 1차 제공 패키지들은 [시맨틱 버전 관리(Semantic Versioning)](https://semver.org)를 따릅니다. 주요 프레임워크 릴리즈는 매년(대략 1분기)에 출시되며, 마이너 및 패치 릴리즈는 매주 출시될 수도 있습니다. 마이너 및 패치 릴리즈에는 절대로 **호환성이 깨지는 변경 사항**이 포함되어서는 안 됩니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 또는 그 구성 요소를 참조할 때는 반드시 `^13.0`과 같은 버전 제약 조건을 사용해야 합니다. Laravel의 메이저 릴리즈에는 호환성이 깨지는 변경 사항이 포함될 수 있기 때문입니다. 그럼에도 저희는 언제나 하루 이내에 새 메이저 릴리즈로 업그레이드할 수 있도록 최선을 다하고 있습니다.

<a name="named-arguments"></a>
#### 네임드 인수

[네임드 인수(named arguments)](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 정책에 포함되지 않습니다. Laravel 코드베이스를 개선하기 위해 필요하다면 함수 인수명을 변경할 수 있습니다. 따라서 Laravel 메서드를 호출할 때 네임드 인수를 사용하는 경우, 향후 파라미터 이름이 바뀔 수 있다는 점을 이해하고 신중하게 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리즈에는 18개월 동안 버그 수정이 제공되며, 2년 동안 보안 수정이 제공됩니다. 추가 라이브러리의 경우 최신 메이저 릴리즈만 버그 수정을 받습니다. 또한 Laravel이 지원하는 데이터베이스 버전에 대해서는 [Laravel이 지원하는 데이터베이스](/docs/13.x/database#introduction) 문서를 참고하시기 바랍니다.

<div class="overflow-auto">

| 버전 | PHP (*) | 릴리즈 | 버그 수정 종료일 | 보안 수정 종료일 |
| --- | --- | --- | --- | --- |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11 | 8.2 - 8.4 | 2024년 3월 12일 | 2025년 9월 3일 | 2026년 3월 12일 |
| 12 | 8.2 - 8.5 | 2025년 2월 24일 | 2026년 8월 13일 | 2027년 2월 24일 |
| 13 | 8.3 - 8.5 | 2026년 1분기 | 2027년 3분기 | 2028년 1분기 |

</div>

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

(*) 지원되는 PHP 버전

<a name="laravel-13"></a>
## Laravel 13

Laravel 13은 Laravel의 연간 릴리즈 주기를 이어가며, AI 중심 워크플로우, 더 강력한 기본값, 그리고 더 표현력 있는 개발자 API에 초점을 맞추고 있습니다. 이번 릴리즈에는 1차 제공 AI 기능, JSON:API 리소스, 시맨틱 / 벡터 검색 기능, 그리고 큐, 캐시, 보안 전반에 걸친 점진적인 개선이 포함됩니다.

<a name="minimal-breaking-changes"></a>
### 최소한의 호환성 깨짐

이번 릴리즈 주기에서 저희가 가장 중점을 둔 부분은 호환성이 깨지는 변경을 최소화하는 것이었습니다. 대신 기존 애플리케이션을 깨뜨리지 않으면서도 연중 계속해서 개발 편의성을 높이는 개선 사항을 제공하는 데 집중했습니다.

따라서 Laravel 13은 도입 노력 측면에서는 비교적 작은 업그레이드이지만, 동시에 상당한 새로운 기능도 제공합니다. 이 때문에 대부분의 Laravel 애플리케이션은 애플리케이션 코드를 많이 바꾸지 않고도 Laravel 13으로 업그레이드할 수 있습니다.

<a name="php-8"></a>
### PHP 8.3

Laravel 13.x는 최소 PHP 8.3을 요구합니다.

<a name="ai-sdk"></a>
### Laravel AI SDK

Laravel 13은 텍스트 생성, 도구 호출 에이전트, 임베딩, 오디오, 이미지, 벡터 스토어 통합을 위한 통합 API를 제공하는 1차 제공 [Laravel AI SDK](https://laravel.com/ai)를 도입합니다.

AI SDK를 사용하면 Laravel에 자연스럽게 녹아드는 일관된 개발 경험을 유지하면서도, 특정 제공자에 종속되지 않는 AI 기능을 구축할 수 있습니다.

예를 들어, 기본 에이전트는 한 번의 호출로 프롬프트를 실행할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;

$response = SalesCoach::make()->prompt('Analyze this sales transcript...');

return (string) $response;
```

Laravel AI SDK는 이미지, 오디오, 임베딩 생성도 지원합니다.

시각적 생성 사용 사례에서는 자연어 프롬프트로 이미지를 생성할 수 있는 깔끔한 API를 제공합니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

음성 경험을 구현할 때는 텍스트로부터 자연스러운 오디오를 합성해 비서, 내레이션, 접근성 기능 등에 활용할 수 있습니다:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

또한 시맨틱 검색과 검색 증강(retrieval) 워크플로우를 위해 문자열에서 직접 임베딩을 생성할 수도 있습니다:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<a name="json-api"></a>
### JSON:API 리소스

Laravel은 이제 1차 제공 [JSON:API 리소스](/docs/13.x/eloquent-resources#jsonapi-resources)를 포함하며, 이를 통해 JSON:API 명세를 준수하는 응답을 훨씬 수월하게 반환할 수 있습니다.

JSON:API 리소스는 리소스 객체 직렬화, 연관관계 포함, sparse fieldset, 링크, 그리고 JSON:API 규격에 맞는 응답 헤더를 처리합니다.

<a name="request-forgery-protection"></a>
### 요청 위조 방지

보안을 위해 Laravel의 [요청 위조 방지](/docs/13.x/csrf#preventing-csrf-requests) 미들웨어가 강화되었고 `PreventRequestForgery`로 공식화되었습니다. 이 미들웨어는 토큰 기반 CSRF 보호와의 호환성을 유지하면서도 origin 인식 요청 검증을 추가합니다.

<a name="queue-routing"></a>
### 큐 라우팅

Laravel 13은 `Queue::route(...)`를 통한 [클래스별 큐 라우팅](/docs/13.x/queues#queue-routing)을 추가했습니다. 이를 통해 특정 작업에 대한 기본 큐 / 연결 라우팅 규칙을 한곳에서 정의할 수 있습니다:

```php
Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
```

<a name="php-attributes"></a>
### 확장된 PHP 속성

Laravel 13은 프레임워크 전반에서 1차 제공 PHP 속성 지원을 계속 확장하고 있습니다. 이를 통해 자주 사용하는 설정과 동작 관련 요소를 더 선언적으로, 그리고 클래스와 메서드 가까이에 배치할 수 있습니다.

대표적으로 [`#[Middleware]`](/docs/13.x/controllers#controller-middleware), [`#[Authorize]`](/docs/13.x/controllers#authorize-attribute) 같은 컨트롤러 및 인가 속성과, [`#[Tries]`](/docs/13.x/queues#max-job-attempts-and-timeout), [`#[Backoff]`](/docs/13.x/queues#dealing-with-failed-jobs), [`#[Timeout]`](/docs/13.x/queues#max-job-attempts-and-timeout), [`#[FailOnTimeout]`](/docs/13.x/queues#failing-on-timeout) 같은 큐 작업 제어 속성이 추가되었습니다.

예를 들어 이제 컨트롤러 미들웨어와 정책 검사를 클래스와 메서드에 직접 선언할 수 있습니다:

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

추가적인 속성들도 Eloquent, 이벤트, 알림, 유효성 검증, 테스트, 리소스 직렬화 API 전반에 도입되어, 프레임워크의 더 많은 영역에서 일관된 attribute-first 선택지를 제공합니다.

<a name="cache-touch"></a>
### 캐시 TTL 연장

Laravel은 이제 [`Cache::touch(...)`](/docs/13.x/cache)를 포함하며, 이를 통해 기존 캐시 항목의 값을 다시 조회하거나 저장하지 않고도 TTL을 연장할 수 있습니다.

<a name="semantic-search"></a>
### 시맨틱 / 벡터 검색

Laravel 13은 [search](/docs/13.x/search#semantic-vector-search), [queries](/docs/13.x/queries#vector-similarity-clauses), 그리고 [AI SDK](/docs/13.x/ai-sdk#embeddings)에 문서화된 네이티브 벡터 쿼리 지원, 임베딩 워크플로우, 관련 API를 통해 시맨틱 검색 스토리를 더욱 강화합니다.

이 기능들을 사용하면 PostgreSQL + `pgvector`를 기반으로, 문자열에서 직접 생성한 임베딩을 활용한 유사도 검색을 포함한 AI 기반 검색 경험을 손쉽게 구축할 수 있습니다.

예를 들어 쿼리 빌더에서 바로 시맨틱 유사도 검색을 수행할 수 있습니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

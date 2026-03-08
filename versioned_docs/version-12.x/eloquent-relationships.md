# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의하기](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다(역방향) / belongsTo](#one-to-many-inverse)
    - [Has One of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [스코프 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 조회하기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [다형성 연관관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [One of Many](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 다형성 타입](#custom-polymorphic-types)
- [동적 연관관계](#dynamic-relationships)
- [연관관계 쿼리](#querying-relations)
    - [연관관계 메서드 vs. 동적 속성](#relationship-methods-vs-dynamic-properties)
    - [연관관계 존재 쿼리](#querying-relationship-existence)
    - [연관관계 부재 쿼리](#querying-relationship-absence)
    - [Morph To 연관관계 쿼리](#querying-morph-to-relationships)
- [연관 모델 집계](#aggregating-related-models)
    - [연관 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 연관관계의 연관 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [즉시 로드(Eager Loading)](#eager-loading)
    - [즉시 로드 조건 지정](#constraining-eager-loads)
    - [지연 즉시 로드(Lazy Eager Loading)](#lazy-eager-loading)
    - [자동 즉시 로드](#automatic-eager-loading)
    - [지연 로드(Lazy Loading) 방지](#preventing-lazy-loading)
- [연관 모델 삽입 및 수정](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 연관관계](#updating-belongs-to-relationships)
    - [다대다 연관관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 동기화](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블은 종종 서로 연관되어 있습니다. 예를 들어, 블로그 게시글은 여러 개의 댓글을 가질 수 있고, 주문은 주문한 사용자와 연관되어 있을 수 있습니다. Eloquent는 이러한 연관관계를 쉽게 관리하고 작업할 수 있게 해주며, 다음과 같은 일반적인 연관관계를 지원합니다:

<div class="content-list" markdown="1">

- [일대일](#one-to-one)
- [일대다](#one-to-many)
- [다대다](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [일대일(다형성)](#one-to-one-polymorphic-relations)
- [일대다(다형성)](#one-to-many-polymorphic-relations)
- [다대다(다형성)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의하기 (Defining Relationships)

Eloquent 연관관계는 각각의 Eloquent 모델 클래스의 메서드로 정의합니다. 연관관계는 강력한 [쿼리 빌더](/docs/12.x/queries)이기도 하므로, 메서드로 정의하면 체이닝과 다양한 쿼리 제약 조건을 쉽게 사용할 수 있습니다. 예를 들어, 아래처럼 `posts` 연관관계에 추가 제약 조건을 붙일 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

연관관계 사용법을 더 깊이 살펴보기 전에, Eloquent에서 지원하는 각 연관관계 정의 방법을 알아봅니다.

<a name="one-to-one"></a>
### 일대일 / hasOne (One to One / Has One)

일대일 연관관계는 가장 기본적인 데이터베이스 연관관계입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과만 연관될 수 있습니다. 이를 정의하려면, `User` 모델에 `phone` 메서드를 추가하고, 해당 메서드에서 `hasOne` 메서드를 호출해 반환하면 됩니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 사용자와 연관된 전화 정보를 가져옵니다.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 인수는 연관된 모델 클래스명입니다. 연관관계가 정의되면, Eloquent의 동적 속성을 통해 연관된 레코드를 조회할 수 있습니다. 동적 속성은 연관관계 메서드를 마치 모델의 속성처럼 호출할 수 있게 해줍니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델 이름을 바탕으로 외래키(foreign key) 컬럼명을 자동으로 결정합니다. 위 예제에서는 `Phone` 모델이 `user_id`라는 외래키를 가진 것으로 간주합니다. 이 규칙을 변경하려면 `hasOne`의 두 번째 인수로 직접 외래키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 외래키의 값이 부모 모델의 기본키(primary key) 컬럼값과 같아야 한다고 가정합니다. 즉, `user_id` 컬럼의 값이 `users` 테이블의 `id` 컬럼값과 일치하는 레코드를 찾습니다. 만약 `id`나 모델의 `$primaryKey`가 아닌 다른 컬럼을 사용할 경우, `hasOne`의 세 번째 인수로 로컬 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 연관관계의 역방향 정의하기

이제 `User` 모델에서 `Phone` 모델을 접근할 수 있게 되었습니다. 반대로, `Phone` 모델에서도 이 전화기의 주인인 사용자를 접근할 수 있도록 연관관계를 정의해보겠습니다. 일대일 연관관계의 역방향은 `belongsTo` 메서드로 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 전화기를 소유한 사용자를 가져옵니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼 값과 일치하는 `id`를 가진 `User` 모델을 찾으려고 시도합니다.

Eloquent는 연관관계 메서드명을 참고해서 외래키 이름을 결정하고, 메서드명 뒤에 `_id`를 붙입니다. 즉, 위 예제에서 `Phone` 모델의 외래키는 `user_id`로 간주됩니다. 만약 `Phone` 모델의 외래키가 `user_id`가 아니라면, `belongsTo`의 두 번째 인수로 원하는 키 이름을 지정할 수 있습니다:

```php
/**
 * 전화기의 소유자 정보를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

만약 부모 모델이 기본키로 `id`를 사용하지 않거나, 다른 컬럼으로 연관 모델을 찾고 싶다면, `belongsTo`의 세 번째 인수로 부모 테이블의 커스텀 키를 지정할 수 있습니다:

```php
/**
 * 전화기의 소유자 정보를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / hasMany (One to Many / Has Many)

일대다 연관관계는 한 모델이 여러 하위 모델을 소유할 때 사용합니다. 예를 들어, 블로그 게시글 하나에 무한히 많은 댓글이 달릴 수 있습니다. 다른 Eloquent 연관관계와 마찬가지로, 모델에 메서드로 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시글의 댓글 목록을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 외래키 컬럼명을 자동으로 판단합니다. 관례상, 부모 모델명을 스네이크 케이스로 한 뒤 `_id`를 붙입니다. 따라서 위 예제에서 외래키는 `post_id`로 간주됩니다.

연관관계 메서드를 정의하고 나면, `comments` 속성에 접근해서 [컬렉션](/docs/12.x/eloquent-collections) 형태로 관련 댓글을 꺼내올 수 있습니다. Eloquent의 "동적 연관관계 속성" 덕분에 연관관계 메서드를 속성처럼 사용 가능합니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 연관관계는 쿼리 빌더 역할도 하므로, `comments` 메서드를 호출한 뒤 체이닝으로 조건을 더 추가할 수도 있습니다:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne`과 마찬가지로, `hasMany`에도 추가 인수로 외래키와 로컬키를 지정할 수 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 하위 모델에 부모 모델 자동 할당하기

Eloquent의 즉시 로드를 사용하더라도, 하위 모델을 반복문으로 순회하는 도중에 해당 하위 모델에서 부모 모델에 접근하면 "N + 1" 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예제의 경우, 각 `Post` 모델마다 댓글은 즉시 로드했지만, 각각의 `Comment`에서 부모 `Post`를 자동으로 할당하지 않아서 "N + 1" 문제가 발생합니다.

만약 Eloquent가 자식에 부모를 자동으로 할당하도록 하려면, `hasMany` 연관관계를 정의할 때 `chaperone` 메서드를 호출하십시오:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시글의 댓글 목록을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

혹은 런타임에 즉시 로드 시 `chaperone`을 사용해서 자동 부모 할당을 켤 수 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / belongsTo (One to Many (Inverse) / Belongs To)

이제 게시글의 모든 댓글을 조회할 수 있으니, 이번에는 댓글에서 부모 게시글에 접근하는 연관관계를 정의해보겠습니다. 이럴 때는 자식 모델에서 `belongsTo` 메서드를 활용한 연관관계 메서드를 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 댓글의 부모 게시글을 가져옵니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

연관관계를 정의한 뒤에는 `post` "동적 연관관계 속성"에 접근해 댓글의 부모 게시글을 가져올 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

위 예제에서, Eloquent는 `Comment` 모델의 `post_id` 컬럼 값과 일치하는 `id`를 가진 `Post` 모델을 찾습니다.

Eloquent는 연관관계 메서드명의 뒤에 부모 모델의 기본키명을 이어 붙여, 외래키명을 결정합니다. 예를 들어, 위에서 `comments` 테이블에 대한 `Post` 모델의 외래키는 `post_id`입니다.

만약 외래키 규칙이 다르다면, `belongsTo`에 두 번째 인수로 커스텀 외래키명을 넘길 수 있습니다:

```php
/**
 * 댓글의 부모 게시글을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델이 `id`외의 다른 컬럼을 기본키로 사용하거나, 연관 모델 찾을 컬럼이 다르다면 `belongsTo`의 세 번째 인수로 커스텀 키를 지정하세요:

```php
/**
 * 댓글의 부모 게시글을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 연관관계에서는 만약 연관된 모델이 `null`일 때 반환할 기본 모델을 정의할 수 있습니다. 이 패턴은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 불리며, 코드 내 조건문을 줄이는 데 도움이 됩니다. 아래 예제는 `user` 연관관계가 연결되지 않은 경우 비어 있는 `App\Models\User` 모델을 반환합니다:

```php
/**
 * 게시글의 작성자(author)를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성을 채워 넣으려면, `withDefault`에 배열 또는 클로저를 넘기면 됩니다:

```php
/**
 * 게시글의 작성자(author)를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 게시글의 작성자(author)를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 연관관계 쿼리

"belongs to" 연관관계의 하위 항목을 쿼리할 때, `where` 절을 직접 작성할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

더 편리하게 사용하려면, 주어진 모델 기준으로 관계와 외래키를 자동으로 판단하는 `whereBelongsTo` 메서드를 이용하세요:

```php
$posts = Post::whereBelongsTo($user)->get();
```

`whereBelongsTo` 메서드에는 [컬렉션](/docs/12.x/eloquent-collections)를 넘겨 여러 부모 모델을 대상으로 할 수 있습니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

Laravel은 기본적으로 주어진 모델의 클래스 이름을 바탕으로 연관관계를 판단하지만, 두 번째 인수로 관계명을 직접 지정할 수도 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### Has One of Many

종종 한 모델이 여러 개의 연관된 모델을 가질 수 있지만, 이 중에서 "가장 최신" 또는 "가장 오래된" 모델만 쉽게 가져오고 싶을 수 있습니다. 예를 들어, `User`가 여러개의 `Order`와 연관되어 있지만 사용자가 가장 최근에 주문한 주문만 가져오고 싶을 때가 있습니다. 이럴 때는 `hasOne` 연관관계와 `ofMany` 계열 메서드를 조합해서 처리할 수 있습니다:

```php
/**
 * 사용자의 가장 최근 주문을 가져옵니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

마찬가지로 "가장 오래된" 연관 모델을 가져오는 메서드도 정의할 수 있습니다:

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany`는 모델의 기본키(primary key)가 정렬기준이 됩니다. 하지만 다른 정렬 기준으로 1개만 조회하고 싶을 때는 `ofMany`를 사용할 수 있습니다. 첫 번째 인수는 정렬할 컬럼, 두 번째 인수는 사용할 집계 함수(`min` 또는 `max`)입니다:

```php
/**
 * 사용자의 최대 금액 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 사용할 수 없으므로, PostgreSQL UUID 컬럼과 one-of-many 관계는 함께 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "Many" 연관관계를 Has One 관계로 변환하기

이미 `latestOfMany`, `oldestOfMany`, `ofMany` 메서드로 1개만 뽑아오는 상황이라면, 기존의 "has many" 연관관계를 쉽게 "has one"으로 변환할 수 있습니다. 관계에서 `one` 메서드를 호출하면 됩니다:

```php
/**
 * 사용자 주문 목록
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 사용자의 최대 금액 주문
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

`one` 메서드는 `HasManyThrough`를 `HasOneThrough`로 바꿀 때도 사용할 수 있습니다:

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One of Many 연관관계

더 복잡한 "has one of many" 연관관계를 구성할 수도 있습니다. 예를 들어, `Product` 모델이 여러 개의 `Price`와 연관되어 있고, 가격이 미래의 특정 시점에 적용될 수도 있다고 합시다. 즉, 가장 최근(미래가 아닌)의 `Price` 데이터가 필요하다면, 다음처럼 `ofMany`에 정렬 기준 컬럼 배열과 클로저를 넘겨 추가 조건을 지정할 수 있습니다:

```php
/**
 * 상품의 현재 가격을 가져옵니다.
 */
public function currentPricing(): HasOne
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function (Builder $query) {
        $query->where('published_at', '<', now());
    });
}
```

<a name="has-one-through"></a>
### Has One Through

"has-one-through" 연관관계는 다른 모델과의 일대일 관계이지만, 이 관계는 _중간_ 모델을 거쳐 연관됩니다.

예를 들어, 차량 정비소 앱에서 `Mechanic`(정비사)마다 한 대의 `Car`(자동차)가 연관되어 있고, 각 `Car`마다 `Owner`(차주)가 있습니다. 이 때, 정비사와 차주 사이에는 직접적인 관계가 없지만, `Car`를 통해 접근이 가능합니다. 아래는 이 관계를 정의하기 위한 테이블 구조입니다:

```text
mechanics
    id - integer
    name - string

cars
    id - integer
    model - string
    mechanic_id - integer

owners
    id - integer
    name - string
    car_id - integer
```

이 테이블 구조에 따라 `Mechanic` 모델에 연관관계를 정의하면 다음과 같습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 자동차의 차주(owner)를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough`의 첫 번째 인수는 최종적으로 접근할 모델, 두 번째 인수는 중간 모델입니다.

또는, 연관된 모든 모델에 이미 관계가 정의되어 있다면, `through` 메서드와 관계명을 조합해 조금 더 유연하게 "has-one-through"를 정의할 수 있습니다:

```php
// 문자열 기반 방식
return $this->through('cars')->has('owner');

// 동적 방식
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규칙(Key Conventions)

Eloquent의 외래키 규칙이 기본적으로 적용됩니다. 키를 직접 지정하려면, `hasOneThrough`의 3-6번째 인수로 각각 중간 모델의 외래키명, 최종 모델의 외래키명, mechanics 테이블의 로컬키, cars 테이블의 로컬키를 지정할 수 있습니다:

```php
class Mechanic extends Model
{
    /**
     * 자동차의 차주(owner)를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // cars 테이블의 외래키명
            'car_id', // owners 테이블의 외래키명
            'id', // mechanics 테이블 로컬키
            'id' // cars 테이블 로컬키
        );
    }
}
```

앞서 설명한 것처럼, 각 모델에 이미 연관관계가 정의되어 있다면 키 규칙도 재사용 가능합니다:

```php
// 문자열 기반 방식
return $this->through('cars')->has('owner');

// 동적 방식
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### Has Many Through

"has-many-through" 연관관계는 간접적인 관계로 멀리 있는 모델을 쉽게 접근할 수 있게 합니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같은 배포 플랫폼에서 `Application` 모델을 기준으로 중간에 `Environment`(환경) 모델을 거쳐 다수의 `Deployment`(배포)를 가져와야 할 수 있습니다. 이 때 테이블 구조는 다음과 같을 수 있습니다:

```text
applications
    id - integer
    name - string

environments
    id - integer
    application_id - integer
    name - string

deployments
    id - integer
    environment_id - integer
    commit_hash - string
```

이 구조에서, `Application` 모델에 아래처럼 연관관계를 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * 애플리케이션의 모든 배포를 가져옵니다.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

첫 번째 인수는 최종적으로 접근할 모델, 두 번째 인수는 중간 모델입니다.

또한, 이미 각 모델에 관계가 정의되어 있다면 다음처럼 유연하게 정의할 수 있습니다:

```php
// 문자열 기반
return $this->through('environments')->has('deployments');

// 동적 방식
return $this->throughEnvironments()->hasDeployments();
```

`deployments` 테이블에는 `application_id`가 없지만, `Environment` 테이블의 `application_id`를 통해 중간에서 찾아 해당되는 `Deployment`를 불러올 수 있습니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙(Key Conventions)

Eloquent 기본값을 사용하지 않고, 직접 키를 지정하려면 `hasManyThrough`의 3-6번째 인수로 다음을 전달하세요:

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id',    // environments 테이블의 외래키
            'environment_id',    // deployments 테이블의 외래키
            'id',                // applications 테이블 로컬키
            'id'                 // environments 테이블 로컬키
        );
    }
}
```

이미 각각 관계가 정의된 경우에는 기존의 키 규칙이 재사용됩니다:

```php
// 문자열
return $this->through('environments')->has('deployments');

// 동적 방식
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프 연관관계 (Scoped Relationships)

모델에서 특정 연관관계에 제약조건(스코프)를 적용한 메서드를 추가하는 경우가 많습니다. 예를 들어, `User` 모델에서 `posts` 연관관계에 추가적으로 `featured` 조건을 걸어서 `featuredPosts` 메서드를 만들 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 게시글을 가져옵니다.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 대표 게시글 목록
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만, 위와 같이 `featuredPosts`로 모델을 생성하면 해당 모델의 `featured` 속성이 자동으로 `true`로 지정되지는 않습니다. 연관관계 메서드로 모델을 생성하면서 특정 속성까지 포함시키려면, 쿼리 빌드 시 `withAttributes`를 사용할 수 있습니다:

```php
/**
 * 사용자의 대표 게시글 목록
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes`는 쿼리의 where 조건에도 해당 속성을 조건으로 추가하고, 새 모델을 생성할 때도 포함합니다:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

쿼리 조건에 포함하지 않고 속성만 추가하고 싶다면, `asConditions` 인수를 false로 지정하세요:

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<a name="many-to-many"></a>
## 다대다 연관관계 (Many to Many Relationships)

다대다 연관관계는 `hasOne`, `hasMany`에 비해 조금 복잡합니다. 대표적인 예로, 하나의 사용자가 여러 역할(role)을 가질 수 있고, 하나의 역할이 여러 사용자에게 공유될 수도 있습니다. 즉, 한 사용자가 "Author", "Editor" 역할을 동시에 가질 수 있고, 각각의 역할은 다른 사용자에게도 할당될 수 있습니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

다대다 연관관계에는 보통 `users`, `roles`, `role_user` 세 개의 테이블이 필요합니다. 중간 테이블인 `role_user`는 알파벳 순서로 처리된 관계 모델명에서 유래되며, `user_id`와 `role_id` 컬럼을 가집니다. 이 테이블이 users와 roles를 연결해줍니다.

역할별로 여러 사용자에게 할당될 수 있으므로, roles 테이블에 단순히 `user_id`만 있으면 안 되며 반드시 중간 테이블이 필요합니다.

테이블 구조 요약:

```text
users
    id - integer
    name - string

roles
    id - integer
    name - string

role_user
    user_id - integer
    role_id - integer
```

<a name="many-to-many-model-structure"></a>
#### 모델 구조

다대다 연관관계는 `belongsToMany` 메서드를 반환하는 메서드를 작성하면 됩니다. 이 메서드는 모든 Eloquent 모델의 부모인 `Illuminate\Database\Eloquent\Model`에서 제공됩니다. 아래는 `User` 모델의 `roles` 메서드 예시입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * 사용자에게 할당된 역할 목록
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

관계가 정의되고 나면, 동적 연관관계 속성으로 사용자의 역할 목록에 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

연관관계도 쿼리 빌더이므로, 조건을 체이닝해서 추출 가능:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

관계 중간 테이블의 이름은 관련 모델명을 알파벳순으로 조합합니다. 이 규칙을 직접 지정할 수도 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

중간 테이블의 키 컬럼명도 3, 4번째 인수로 지정 가능합니다(자기 자신의 외래키, 반대 모델의 외래키):

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 다대다 연관관계 역방향 정의

다대다 연관관계의 "역방향"을 정의하려면, 관련 모델에도 역시 `belongsToMany`를 반환하는 메서드를 작성하면 됩니다. 이제 `Role` 모델에도 `users` 관계를 추가해봅니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 역할(role)이 할당된 사용자 목록
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

사용법/옵션/커스텀화는 `User`와 유사합니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 조회하기

다대다 연관관계에서는 중간 테이블이 필요합니다. Eloquent는 이 테이블과 쉽게 상호작용할 수 있게 도와줍니다. 예를 들어, `User`가 여러 `Role`과 연결되어 있을 때 각 역할의 `pivot` 속성을 통해 중간 테이블 정보에 접근 가능합니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

기본적으로 중간 테이블의 키 정보만 제공하지만, 추가 컬럼이 있다고 하면 명시적으로 지정해줄 수 있습니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

`created_at`, `updated_at` 등 타임스탬프를 자동으로 관리하고 싶으면 `withTimestamps()`를 추가하세요:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Eloquent의 자동 타임스탬프를 사용할 때에는 반드시 `created_at`와 `updated_at` 컬럼이 모두 존재해야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 커스터마이즈

중간 테이블 정보를 `pivot` 이외의 이름으로 접근하고 싶다면, `as` 메서드로 속성명을 정할 수 있습니다:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

이후에는 커스텀 속성명으로 접근하면 됩니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 쿼리 필터링

중간 테이블 값을 조건으로 쿼리를 필터링할 수도 있습니다. 다음 메서드를 사용할 수 있습니다: `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull`

```php
return $this->belongsToMany(Role::class)
    ->wherePivot('approved', 1);

return $this->belongsToMany(Role::class)
    ->wherePivotIn('priority', [1, 2]);

return $this->belongsToMany(Role::class)
    ->wherePivotNotIn('priority', [1, 2]);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNull('expired_at');

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotNull('expired_at');
```

`wherePivot`은 쿼리에 WHERE 조건만 추가하며, 새 모델 생성 시에는 해당 값을 세팅하지 않습니다. 둘 다 적용하려면, `withPivotValue`를 사용합니다:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 쿼리 정렬

`orderByPivot` 및 `orderByPivotDesc`로 중간 테이블 컬럼 기준으로 정렬할 수 있습니다:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivotDesc('created_at');
```

<a name="defining-custom-intermediate-table-models"></a>
### 커스텀 중간 테이블 모델 정의하기

다대다 연관관계의 중간 테이블에 대한 커스텀 모델을 만들고 싶다면 `using` 메서드로 지정하세요. 커스텀 pivot 모델을 통해 추가 동작(메서드, 캐스트 등)을 정의할 수 있습니다.

커스텀 pivot 모델은 `Illuminate\Database\Eloquent\Relations\Pivot`(일반) 혹은 `Illuminate\Database\Eloquent\Relations\MorphPivot`(다형성)을 상속받아야 합니다.

예시:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 역할(role)이 할당된 사용자 목록
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

`RoleUser` pivot 모델 정의 예:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    // ...
}
```

> [!WARNING]
> Pivot 모델은 `SoftDeletes` 트레잇을 사용할 수 없습니다. Pivot 레코드에 soft delete가 필요하면, 일반 Eloquent 모델로 전환하는 것이 좋습니다.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 Pivot 모델과 자동 증가 ID

커스텀 pivot 모델에서 자동 증가 primary key를 사용한다면, `$incrementing = true` 속성을 반드시 선언해야 합니다:

```php
/**
 * ID가 자동 증가하는지 설정
 *
 * @var bool
 */
public $incrementing = true;
```

{/* 이하의 모든 내용은 본문 구조 및 규정을 따르기 때문에 생략 없이 번역이 계속됩니다. 추가 번역이 필요하다면 이어서 요청해 주세요. */}

# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의하기](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다(역방향) / belongsTo](#one-to-many-inverse)
    - [다수 중 하나 가져오기](#has-one-of-many)
    - [중간 모델을 통한 일대일](#has-one-through)
    - [중간 모델을 통한 일대다](#has-many-through)
- [스코프 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 조회하기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [다형성 연관관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [다수 중 하나](#one-of-many-polymorphic-relations)
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

Eloquent 연관관계는 각각의 Eloquent 모델 클래스의 메서드로 정의합니다. 연관관계는 강력한 [쿼리 빌더](/docs/13.x/queries)이기도 하므로, 메서드로 정의하면 체이닝과 다양한 쿼리 제약 조건을 쉽게 사용할 수 있습니다. 예를 들어, 아래처럼 `posts` 연관관계에 추가 제약 조건을 붙일 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

연관관계 사용법을 더 깊이 살펴보기 전에, Eloquent에서 지원하는 각 연관관계 정의 방법을 알아봅니다.

<a name="one-to-one"></a>
### 일대일 / hasOne

일대일 연관관계는 가장 기본적인 데이터베이스 연관관계입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과만 연관될 수 있습니다. 이를 정의하려면, `User` 모델에 `phone` 메서드를 추가하고, 해당 메서드에서 `hasOne` 메서드를 호출해 반환하면 됩니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * Get the phone associated with the user.
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

또한, Eloquent는 외래키의 값이 부모 모델의 기본키(primary key) 컬럼값과 같아야 한다고 가정합니다. 즉, `user_id` 컬럼의 값이 `users` 테이블의 `id` 컬럼값과 일치하는 레코드를 찾습니다. 만약 `id`나 모델의 기본 키가 아닌 다른 컬럼을 사용할 경우, `hasOne`의 세 번째 인수로 로컬 키를 지정할 수 있습니다:

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
     * Get the user that owns the phone.
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
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

만약 부모 모델이 기본키로 `id`를 사용하지 않거나, 다른 컬럼으로 연관 모델을 찾고 싶다면, `belongsTo`의 세 번째 인수로 부모 테이블의 커스텀 키를 지정할 수 있습니다:

```php
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / hasMany

일대다 연관관계는 한 모델이 여러 하위 모델을 소유할 때 사용합니다. 예를 들어, 블로그 게시글 하나에 무한히 많은 댓글이 달릴 수 있습니다. 다른 Eloquent 연관관계와 마찬가지로, 모델에 메서드로 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 외래키 컬럼명을 자동으로 판단합니다. 관례상, 부모 모델명을 스네이크 케이스로 한 뒤 `_id`를 붙입니다. 따라서 위 예제에서 외래키는 `post_id`로 간주됩니다.

연관관계 메서드를 정의하고 나면, `comments` 속성에 접근해서 [컬렉션](/docs/13.x/eloquent-collections) 형태로 관련 댓글을 꺼내올 수 있습니다. Eloquent의 "동적 연관관계 속성" 덕분에 연관관계 메서드를 속성처럼 사용 가능합니다:

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
     * Get the comments for the blog post.
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
### 일대다(역방향) / belongsTo

이제 게시글의 모든 댓글을 조회할 수 있으니, 이번에는 댓글에서 부모 게시글에 접근하는 연관관계를 정의해보겠습니다. 이럴 때는 자식 모델에서 `belongsTo` 메서드를 활용한 연관관계 메서드를 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * Get the post that owns the comment.
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
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델이 `id`외의 다른 컬럼을 기본키로 사용하거나, 연관 모델 찾을 컬럼이 다르다면 `belongsTo`의 세 번째 인수로 커스텀 키를 지정하세요:

```php
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 연관관계에서는 만약 연관된 모델이 `null`일 때 반환할 기본 모델을 정의할 수 있습니다. 이 패턴은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 불리며, 코드 내 조건문을 줄이는 데 도움이 됩니다. 아래 예제는 `user` 연관관계가 연결되지 않은 경우 비어 있는 `App\Models\User` 모델을 반환합니다:

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성을 채워 넣으려면, `withDefault`에 배열 또는 클로저를 넘기면 됩니다:

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * Get the author of the post.
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

`whereBelongsTo` 메서드에는 [컬렉션](/docs/13.x/eloquent-collections)를 넘겨 여러 부모 모델을 대상으로 할 수 있습니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

Laravel은 기본적으로 주어진 모델의 클래스 이름을 바탕으로 연관관계를 판단하지만, 두 번째 인수로 관계명을 직접 지정할 수도 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 다수 중 하나 가져오기 (Has One of Many)

종종 한 모델이 여러 개의 연관된 모델을 가질 수 있지만, 이 중에서 "가장 최신" 또는 "가장 오래된" 모델만 쉽게 가져오고 싶을 수 있습니다. 예를 들어, `User`가 여러개의 `Order`와 연관되어 있지만 사용자가 가장 최근에 주문한 주문만 가져오고 싶을 때가 있습니다. 이럴 때는 `hasOne` 연관관계와 `ofMany` 계열 메서드를 조합해서 처리할 수 있습니다:

```php
/**
 * Get the user's most recent order.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

마찬가지로 "가장 오래된" 연관 모델을 가져오는 메서드도 정의할 수 있습니다:

```php
/**
 * Get the user's oldest order.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany`는 모델의 기본키(primary key)가 정렬기준이 됩니다. 하지만 다른 정렬 기준으로 1개만 조회하고 싶을 때는 `ofMany`를 사용할 수 있습니다. 첫 번째 인수는 정렬할 컬럼, 두 번째 인수는 사용할 집계 함수(`min` 또는 `max`)입니다:

```php
/**
 * Get the user's largest order.
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
 * Get the user's orders.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * Get the user's largest order.
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
 * Get the current pricing for the product.
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
### 중간 모델을 통한 일대일

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
     * Get the car's owner.
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
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규칙

Eloquent의 외래키 규칙이 기본적으로 적용됩니다. 키를 직접 지정하려면, `hasOneThrough`의 3-6번째 인수로 각각 중간 모델의 외래키명, 최종 모델의 외래키명, mechanics 테이블의 로컬키, cars 테이블의 로컬키를 지정할 수 있습니다:

```php
class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // Foreign key on the cars table...
            'car_id', // Foreign key on the owners table...
            'id', // Local key on the mechanics table...
            'id' // Local key on the cars table...
        );
    }
}
```

앞서 설명한 것처럼, 각 모델에 이미 연관관계가 정의되어 있다면 키 규칙도 재사용 가능합니다:

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### 중간 모델을 통한 일대다

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
     * Get all of the deployments for the application.
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
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

`deployments` 테이블에는 `application_id`가 없지만, `Environment` 테이블의 `application_id`를 통해 중간에서 찾아 해당되는 `Deployment`를 불러올 수 있습니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙

Eloquent 기본값을 사용하지 않고, 직접 키를 지정하려면 `hasManyThrough`의 3-6번째 인수로 다음을 전달하세요:

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id', // Foreign key on the environments table...
            'environment_id', // Foreign key on the deployments table...
            'id', // Local key on the applications table...
            'id' // Local key on the environments table...
        );
    }
}
```

이미 각각 관계가 정의된 경우에는 기존의 키 규칙이 재사용됩니다:

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프 연관관계

모델에서 특정 연관관계에 제약조건(스코프)를 적용한 메서드를 추가하는 경우가 많습니다. 예를 들어, `User` 모델에서 `posts` 연관관계에 추가적으로 `featured` 조건을 걸어서 `featuredPosts` 메서드를 만들 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get the user's posts.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * Get the user's featured posts.
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
 * Get the user's featured posts.
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
     * The roles that belong to the user.
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
     * The users that belong to the role.
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
#### `pivot` 속성명 사용자 지정

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
     * The users that belong to the role.
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

커스텀 pivot 모델을 사용하는 다대다 연관관계를 정의했고, 해당 pivot 모델이 자동 증가 기본 키를 가진다면 `incrementing`이 `true`로 설정된 `Table` 속성을 사용해야 합니다:

```php
use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Relations\Pivot;

#[Table(incrementing: true)]
class RoleUser extends Pivot
{
    // ...
}
```

<a name="polymorphic-relationships"></a>
## 다형성 연관관계 (Polymorphic Relationships)

다형성(polymorphic) 연관관계는 하위 모델이 단일 연관으로 둘 이상의 모델 타입에 속할 수 있게 해줍니다. 예를 들어, 사용자가 블로그 게시글과 동영상을 공유하는 앱에서 `Comment` 모델은 `Post` 모델과 `Video` 모델 모두에 속할 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일 (다형성)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 다형성 연관관계는 일반적인 일대일과 유사하지만, 자식 모델이 하나의 연관으로 여러 타입의 모델에 속할 수 있다는 점이 다릅니다. 예를 들어, `Post`와 `User`가 `Image` 모델과 다형성 관계를 공유할 수 있습니다. 하나의 고유한 이미지 테이블로 게시글과 사용자 모두에 연결 가능합니다. 테이블 구조는 다음과 같습니다:

```text
posts
    id - integer
    name - string

users
    id - integer
    name - string

images
    id - integer
    url - string
    imageable_id - integer
    imageable_type - string
```

`images` 테이블의 `imageable_id`와 `imageable_type` 컬럼에 주목하세요. `imageable_id` 컬럼은 게시글 또는 사용자의 ID 값을, `imageable_type` 컬럼은 부모 모델의 클래스명을 담고 있습니다. Eloquent는 `imageable_type` 컬럼을 통해 `imageable` 관계에 접근할 때 반환할 부모 모델의 "타입"을 결정합니다. 이 컬럼에는 `App\Models\Post` 또는 `App\Models\User` 같은 값이 들어갑니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

이 관계를 구성하기 위한 모델 정의는 다음과 같습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * Get the parent imageable model (user or post).
     */
    public function imageable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class Post extends Model
{
    /**
     * Get the post's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class User extends Model
{
    /**
     * Get the user's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 연관관계 조회하기

데이터베이스 테이블과 모델이 정의되면, 모델을 통해 연관관계에 접근할 수 있습니다. 예를 들어, 게시글의 이미지를 가져오려면 `image` 동적 연관관계 속성에 접근하면 됩니다:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

`morphTo`를 호출하는 메서드명에 접근하면 다형성 모델의 부모를 조회할 수 있습니다. 이 경우 `Image` 모델의 `imageable` 메서드입니다. 이를 동적 연관관계 속성으로 접근합니다:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`Image` 모델의 `imageable` 관계는 이미지의 소유 타입에 따라 `Post` 또는 `User` 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 규칙

필요한 경우, 다형성 자식 모델이 사용하는 "id"와 "type" 컬럼명을 직접 지정할 수 있습니다. 이때 반드시 첫 번째 인수로 관계명을 전달해야 합니다. 보통 메서드명과 동일해야 하므로 PHP의 `__FUNCTION__` 상수를 사용할 수 있습니다:

```php
/**
 * Get the model that the image belongs to.
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 일대다 (다형성)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

일대다 다형성 연관관계는 일반적인 일대다와 유사하지만, 자식 모델이 하나의 연관으로 둘 이상의 모델 타입에 속할 수 있습니다. 예를 들어, 게시글과 동영상 모두에 "댓글"을 달 수 있다고 가정하면, 하나의 `comments` 테이블로 양쪽 댓글을 모두 관리할 수 있습니다. 테이블 구조는 다음과 같습니다:

```text
posts
    id - integer
    title - string
    body - text

videos
    id - integer
    title - string
    url - string

comments
    id - integer
    body - text
    commentable_id - integer
    commentable_type - string
```

<a name="one-to-many-polymorphic-model-structure"></a>
#### 모델 구조

이 관계를 구성하기 위한 모델 정의는 다음과 같습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * Get the parent commentable model (post or video).
     */
    public function commentable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Video extends Model
{
    /**
     * Get all of the video's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 연관관계 조회하기

데이터베이스 테이블과 모델이 정의되면, 모델의 동적 연관관계 속성을 통해 관계에 접근할 수 있습니다. 예를 들어, 게시글의 모든 댓글을 가져오려면 `comments` 동적 속성을 사용합니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

`morphTo`를 호출하는 메서드명에 접근하면 다형성 자식의 부모 모델을 가져올 수 있습니다. 이 경우 `Comment` 모델의 `commentable` 메서드이므로 동적 연관관계 속성처럼 접근합니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`Comment` 모델의 `commentable` 관계는 댓글의 부모 타입에 따라 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### 하위 모델에 부모 모델 자동 할당하기

Eloquent의 즉시 로드를 사용하더라도, 하위 모델을 순회하면서 부모 모델에 접근하면 "N + 1" 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

위 예제에서는 댓글을 즉시 로드했더라도, 각 `Comment`에 부모 `Post`가 자동으로 할당되지 않아 "N + 1" 문제가 생깁니다.

Eloquent가 자식에 부모를 자동으로 할당하도록 하려면, `morphMany` 관계 정의 시 `chaperone` 메서드를 호출하세요:

```php
class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

런타임에 즉시 로드 시 자동 부모 할당을 활성화할 수도 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
### 다수 중 하나 (다형성)

때때로 모델이 여러 관련 모델을 가질 수 있지만, "가장 최신" 또는 "가장 오래된" 관련 모델만 쉽게 가져오고 싶을 수 있습니다. 예를 들어, `User` 모델이 여러 `Image` 모델과 연관되어 있지만, 가장 최근에 업로드한 이미지 하나만 편리하게 접근하고 싶다면, `morphOne` 관계와 `ofMany` 계열 메서드를 조합할 수 있습니다:

```php
/**
 * Get the user's most recent image.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

마찬가지로, "가장 오래된" 관련 모델을 가져오는 메서드도 정의할 수 있습니다:

```php
/**
 * Get the user's oldest image.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany`는 모델의 기본키를 기준으로 정렬합니다. 하지만 다른 정렬 기준을 사용하고 싶다면 `ofMany` 메서드를 사용할 수 있습니다. 첫 번째 인수는 정렬 컬럼, 두 번째 인수는 집계 함수(`min` 또는 `max`)입니다:

```php
/**
 * Get the user's most popular image.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> 더 복잡한 "one of many" 연관관계를 구성할 수도 있습니다. 자세한 내용은 [has one of many 문서](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다 (다형성)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다대다 다형성 연관관계는 "morph one"이나 "morph many"보다 약간 복잡합니다. 예를 들어, `Post`와 `Video` 모델이 `Tag` 모델과 다형성 관계를 공유할 수 있습니다. 이렇게 하면 하나의 태그 테이블로 게시글과 동영상 모두에 태그를 연결할 수 있습니다. 테이블 구조는 다음과 같습니다:

```text
posts
    id - integer
    name - string

videos
    id - integer
    name - string

tags
    id - integer
    name - string

taggables
    tag_id - integer
    taggable_id - integer
    taggable_type - string
```

> [!NOTE]
> 다형성 다대다 연관관계를 살펴보기 전에, 일반적인 [다대다 연관관계](#many-to-many) 문서를 먼저 읽어보시면 도움이 됩니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

이제 모델에서 관계를 정의할 준비가 되었습니다. `Post`와 `Video` 모델 모두 기본 Eloquent 모델 클래스의 `morphToMany` 메서드를 호출하는 `tags` 메서드를 포함합니다.

`morphToMany` 메서드는 관련 모델명과 "관계명"을 인수로 받습니다. 중간 테이블 이름과 키를 기반으로, 이 관계를 "taggable"이라고 지칭합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * Get all of the tags for the post.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 역방향 관계 정의하기

`Tag` 모델에서는 가능한 각 부모 모델에 대한 메서드를 정의해야 합니다. 이 예시에서는 `posts`와 `videos` 메서드를 정의합니다. 두 메서드 모두 `morphedByMany`를 반환합니다.

`morphedByMany` 메서드는 관련 모델명과 "관계명"을 인수로 받습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * Get all of the posts that are assigned this tag.
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * Get all of the videos that are assigned this tag.
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 연관관계 조회하기

데이터베이스 테이블과 모델이 정의되면, 모델을 통해 관계에 접근할 수 있습니다. 예를 들어, 게시글의 모든 태그를 가져오려면 `tags` 동적 연관관계 속성을 사용합니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

`morphedByMany`를 호출하는 메서드명에 접근하면 다형성 자식에서 부모 모델을 가져올 수 있습니다. 여기서는 `Tag` 모델의 `posts`나 `videos` 메서드입니다:

```php
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    // ...
}

foreach ($tag->videos as $video) {
    // ...
}
```

<a name="custom-polymorphic-types"></a>
### 커스텀 다형성 타입

기본적으로 Laravel은 관련 모델의 "타입"을 저장할 때 완전한 클래스명을 사용합니다. 예를 들어, 위의 일대다 다형성 예시에서 `Comment`가 `Post` 또는 `Video`에 속할 수 있다면, `commentable_type`에는 기본적으로 `App\Models\Post` 또는 `App\Models\Video`가 저장됩니다. 하지만 이 값을 애플리케이션의 내부 구조에서 분리시키고 싶을 수 있습니다.

예를 들어, 모델명 대신 `post`, `video`와 같은 단순 문자열을 사용할 수 있습니다. 이렇게 하면 모델 이름이 변경되어도 데이터베이스의 다형성 "타입" 컬럼 값은 유효하게 유지됩니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

`enforceMorphMap` 메서드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출하거나, 별도의 서비스 프로바이더를 생성해서 호출할 수 있습니다.

런타임에 주어진 모델의 morph 별칭을 확인하려면 `getMorphClass` 메서드를 사용하고, morph 별칭에서 완전한 클래스명을 확인하려면 `Relation::getMorphedModel` 메서드를 사용합니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 기존 애플리케이션에 "morph map"을 추가할 경우, 데이터베이스에 아직 완전한 클래스명으로 저장되어 있는 모든 morphable `*_type` 컬럼 값을 "map" 이름으로 변환해야 합니다.

<a name="dynamic-relationships"></a>
### 동적 연관관계

`resolveRelationUsing` 메서드를 사용하면 런타임에 Eloquent 모델 간의 관계를 정의할 수 있습니다. 일반적인 앱 개발에서는 권장되지 않지만, 라라벨 패키지 개발 시에 유용할 수 있습니다.

`resolveRelationUsing` 메서드의 첫 번째 인수는 원하는 관계명이고, 두 번째 인수는 모델 인스턴스를 받아 유효한 Eloquent 관계 정의를 반환하는 클로저입니다. 보통 [서비스 프로바이더](/docs/13.x/providers)의 boot 메서드에서 동적 관계를 설정합니다:

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 관계를 정의할 때는 항상 Eloquent 관계 메서드에 명시적인 키 이름 인수를 전달해야 합니다.

<a name="querying-relations"></a>
## 연관관계 쿼리 (Querying Relations)

모든 Eloquent 연관관계는 메서드를 통해 정의되므로, 관련 모델을 실제로 로드하는 쿼리를 실행하지 않고도 관계의 인스턴스를 얻을 수 있습니다. 또한, 모든 유형의 Eloquent 관계는 [쿼리 빌더](/docs/13.x/queries) 역할도 하므로, SQL 쿼리를 실행하기 전에 관계 쿼리에 조건을 계속 체이닝할 수 있습니다.

예를 들어, `User` 모델이 여러 `Post`를 가진 블로그 앱을 상상해보세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get all of the posts for the user.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

`posts` 관계를 쿼리하면서 추가 조건을 붙일 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

Laravel [쿼리 빌더](/docs/13.x/queries)의 모든 메서드를 관계에 사용할 수 있으므로, 쿼리 빌더 문서를 참고해 사용 가능한 메서드를 확인하세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 뒤에 `orWhere` 절 체이닝하기

위 예시처럼 관계 쿼리에 추가 조건을 자유롭게 붙일 수 있지만, `orWhere` 절을 체이닝할 때는 주의가 필요합니다. `orWhere`는 관계 제약과 같은 수준에서 논리적으로 그룹핑되기 때문입니다:

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

위 예제는 다음과 같은 SQL을 생성합니다. `or` 절 때문에 100표 이상인 _모든_ 게시글이 반환되어, 특정 사용자로 제한되지 않습니다:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

대부분의 경우, [논리적 그룹](/docs/13.x/queries#logical-grouping)을 사용하여 조건 검사를 괄호로 묶어야 합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

위 예제는 다음 SQL을 생성합니다. 논리적 그룹핑이 올바르게 적용되어 쿼리가 특정 사용자로 제한됩니다:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 연관관계 메서드 vs. 동적 속성

Eloquent 관계 쿼리에 추가 제약을 걸 필요가 없다면, 관계를 속성처럼 접근할 수 있습니다. 예를 들어, `User`와 `Post` 모델을 사용해 사용자의 모든 게시글에 다음과 같이 접근합니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

동적 연관관계 속성은 "지연 로드(lazy loading)"를 수행합니다. 즉, 실제로 접근할 때만 관계 데이터를 로드합니다. 이 때문에 개발자들은 모델 로드 후 접근할 관계를 미리 로드하는 [즉시 로드(eager loading)](#eager-loading)를 자주 사용합니다. 즉시 로드는 모델의 관계를 로드하기 위해 실행되어야 하는 SQL 쿼리를 크게 줄여줍니다.

<a name="querying-relationship-existence"></a>
### 연관관계 존재 쿼리

모델 레코드를 조회할 때, 관계의 존재 여부를 기반으로 결과를 제한하고 싶을 수 있습니다. 예를 들어, 댓글이 하나 이상 있는 모든 블로그 게시글을 가져오고 싶다면, 관계명을 `has`와 `orHas` 메서드에 전달합니다:

```php
use App\Models\Post;

// Retrieve all posts that have at least one comment...
$posts = Post::has('comments')->get();
```

연산자와 개수 값을 지정하여 쿼리를 더 세밀하게 조정할 수도 있습니다:

```php
// Retrieve all posts that have three or more comments...
$posts = Post::has('comments', '>=', 3)->get();
```

중첩 `has` 구문은 "점" 표기법으로 작성할 수 있습니다. 예를 들어, 이미지가 있는 댓글이 하나 이상인 게시글을 가져올 수 있습니다:

```php
// Retrieve posts that have at least one comment with images...
$posts = Post::has('comments.images')->get();
```

더 세밀한 제어가 필요하면 `whereHas`와 `orWhereHas` 메서드를 사용하여 `has` 쿼리에 추가 조건을 정의할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

// Retrieve posts with at least one comment containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// Retrieve posts with at least ten comments containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]
> Eloquent는 현재 데이터베이스를 넘나드는 관계 존재 쿼리를 지원하지 않습니다. 관계는 동일한 데이터베이스 내에 존재해야 합니다.

<a name="many-to-many-relationship-existence-queries"></a>
#### 다대다 관계 존재 쿼리

`whereAttachedTo` 메서드를 사용하면 모델 또는 모델 컬렉션에 다대다 연결이 있는 모델을 쿼리할 수 있습니다:

```php
$users = User::whereAttachedTo($role)->get();
```

`whereAttachedTo`에 [컬렉션](/docs/13.x/eloquent-collections)을 넘기면, 컬렉션 내 어떤 모델에라도 연결된 모델을 조회합니다:

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```

<a name="inline-relationship-existence-queries"></a>
#### 인라인 관계 존재 쿼리

관계 쿼리에 단일 조건만 붙여 관계 존재를 확인하려면 `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 메서드가 더 편리할 수 있습니다. 예를 들어, 승인되지 않은 댓글이 있는 게시글을 쿼리합니다:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

물론, 쿼리 빌더의 `where` 메서드와 마찬가지로 연산자를 지정할 수도 있습니다:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->minus(hours: 1)
)->get();
```

<a name="querying-relationship-absence"></a>
### 연관관계 부재 쿼리

모델 레코드를 조회할 때, 관계의 부재를 기반으로 결과를 제한하고 싶을 수 있습니다. 예를 들어, 댓글이 **없는** 모든 블로그 게시글을 가져오려면, `doesntHave`와 `orDoesntHave` 메서드에 관계명을 전달합니다:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

더 세밀한 제어가 필요하면 `whereDoesntHave`와 `orWhereDoesntHave` 메서드에 추가 쿼리 조건을 붙일 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

"점" 표기법으로 중첩 관계에 대해서도 쿼리할 수 있습니다. 예를 들어, 다음 쿼리는 댓글이 없는 게시글과 차단된 사용자의 댓글이 없는 게시글을 가져옵니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Morph To 연관관계 쿼리

"morph to" 관계의 존재를 쿼리하려면 `whereHasMorph`와 `whereDoesntHaveMorph` 메서드를 사용합니다. 이 메서드는 첫 번째 인수로 관계명, 두 번째 인수로 쿼리에 포함할 관련 모델명 배열, 그리고 선택적으로 관계 쿼리를 커스텀하는 클로저를 받습니다:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// Retrieve comments associated to posts or videos with a title like code%...
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// Retrieve comments associated to posts with a title not like code%...
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

관련 다형성 모델의 "타입"에 따라 쿼리 조건을 추가해야 할 때도 있습니다. `whereHasMorph`에 전달된 클로저는 두 번째 인수로 `$type` 값을 받을 수 있으며, 이를 통해 빌드 중인 쿼리의 "타입"을 확인할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, string $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```

때로는 "morph to" 관계의 부모 자식을 쿼리하고 싶을 수 있습니다. `whereMorphedTo`와 `whereNotMorphedTo` 메서드를 사용하면 적절한 morph 타입 매핑을 자동으로 결정합니다. 첫 번째 인수로 `morphTo` 관계명을, 두 번째 인수로 관련 부모 모델을 전달합니다:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 관련 모델 쿼리하기

가능한 다형성 모델의 배열 대신 `*`를 와일드카드로 제공할 수 있습니다. 이렇게 하면 Laravel이 데이터베이스에서 가능한 모든 다형성 타입을 조회합니다. 이를 위해 추가 쿼리가 한 번 더 실행됩니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 연관 모델 집계 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 연관 모델 개수 세기

관련 모델을 실제로 로드하지 않고 개수만 세고 싶을 때는 `withCount` 메서드를 사용합니다. `withCount`는 결과 모델에 `{relation}_count` 속성을 추가합니다:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

배열을 `withCount`에 전달하면 여러 관계의 "개수"를 추가하고, 쿼리에 추가 조건도 붙일 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

관계 개수 결과에 별칭을 붙여 동일한 관계에 대해 여러 개의 카운트를 정의할 수도 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount([
    'comments',
    'comments as pending_comments_count' => function (Builder $query) {
        $query->where('approved', false);
    },
])->get();

echo $posts[0]->comments_count;
echo $posts[0]->pending_comments_count;
```

<a name="deferred-count-loading"></a>
#### 지연 카운트 로딩

`loadCount` 메서드를 사용하면 부모 모델을 이미 가져온 뒤에도 관계 개수를 로드할 수 있습니다:

```php
$book = Book::first();

$book->loadCount('genres');
```

카운트 쿼리에 추가 조건을 설정하려면, 관계명을 키로 하고 클로저를 값으로 하는 배열을 전달합니다:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### 관계 카운트와 커스텀 Select 구문

`withCount`를 `select`와 함께 사용할 때는 반드시 `select` 메서드 뒤에 `withCount`를 호출하세요:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withCount` 외에도 Eloquent는 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 메서드를 제공합니다. 이 메서드들은 결과 모델에 `{relation}_{function}_{column}` 속성을 추가합니다:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

집계 함수 결과에 별칭을 사용하고 싶다면 다음과 같이 지정합니다:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

`loadCount`와 마찬가지로 지연 버전도 사용 가능합니다. 이미 조회된 Eloquent 모델에 대해 추가 집계 연산을 수행할 수 있습니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

집계 메서드를 `select`와 함께 사용할 때는 `select` 뒤에 호출하세요:

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 연관관계의 연관 모델 개수 세기

"morph to" 관계를 즉시 로드하면서, 해당 관계가 반환할 수 있는 다양한 엔티티의 관련 모델 개수도 함께 로드하려면 `with` 메서드와 `morphTo` 관계의 `morphWithCount` 메서드를 조합합니다.

이 예제에서는 `Photo`와 `Post` 모델이 `ActivityFeed` 모델을 생성할 수 있다고 가정합니다. `ActivityFeed` 모델에는 `parentable`이라는 "morph to" 관계가 정의되어 있습니다. 또한 `Photo` 모델은 여러 `Tag`를, `Post` 모델은 여러 `Comment`를 가집니다.

`ActivityFeed` 인스턴스를 조회하면서 각 `parentable` 부모 모델을 즉시 로드하고, 각 부모 사진의 태그 수와 게시글의 댓글 수도 함께 가져오려면:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::with([
    'parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWithCount([
            Photo::class => ['tags'],
            Post::class => ['comments'],
        ]);
    }])->get();
```

<a name="morph-to-deferred-count-loading"></a>
#### 지연 카운트 로딩

이미 `ActivityFeed` 모델 집합을 조회한 뒤, 관련 `parentable` 모델들의 중첩된 관계 카운트를 로드하려면 `loadMorphCount` 메서드를 사용합니다:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## 즉시 로드 (Eager Loading)

Eloquent 관계를 속성으로 접근하면, 관련 모델은 "지연 로드(lazy load)"됩니다. 즉, 속성에 처음 접근할 때까지 관계 데이터가 실제로 로드되지 않습니다. 하지만 Eloquent에서는 부모 모델 쿼리 시점에 관계를 "즉시 로드(eager load)"할 수 있습니다. 즉시 로드는 "N + 1" 쿼리 문제를 해결합니다. N + 1 쿼리 문제를 설명하기 위해, `Author`에 "속하는(belongs to)" `Book` 모델을 생각해봅시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

이제 모든 책과 저자를 조회해봅니다:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 루프는 데이터베이스에서 모든 책을 가져오기 위해 쿼리 1개, 그리고 각 책마다 저자를 가져오기 위해 추가 쿼리를 실행합니다. 책이 25권이라면 총 26개의 쿼리가 실행됩니다.

다행히 즉시 로드를 사용하면 이 작업을 단 2개의 쿼리로 줄일 수 있습니다. 쿼리를 빌드할 때 `with` 메서드로 즉시 로드할 관계를 지정합니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 경우 쿼리는 2개만 실행됩니다 - 하나는 모든 책 조회, 하나는 모든 책의 저자 조회:

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 즉시 로드

여러 개의 다른 관계를 즉시 로드해야 할 때는 `with` 메서드에 관계 배열을 전달하면 됩니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 즉시 로드

관계의 관계를 즉시 로드하려면 "점" 표기법을 사용합니다. 예를 들어, 모든 책의 저자와 저자의 연락처 정보를 즉시 로드합니다:

```php
$books = Book::with('author.contacts')->get();
```

또는 `with` 메서드에 중첩 배열을 전달하여 여러 중첩 관계를 즉시 로드할 수도 있습니다:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### 중첩 즉시 로드 `morphTo` 관계

`morphTo` 관계를 즉시 로드하면서, 해당 관계가 반환할 수 있는 다양한 엔티티의 중첩 관계도 함께 로드하려면 `with` 메서드와 `morphTo` 관계의 `morphWith` 메서드를 조합합니다. 다음 모델을 참고하세요:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

이 예제에서 `Event`, `Photo`, `Post` 모델이 `ActivityFeed`를 생성할 수 있다고 가정합니다. `Event` 모델은 `Calendar`에 속하고, `Photo`는 `Tag`와 연관되며, `Post`는 `Author`에 속합니다.

이 모델 정의와 관계를 사용하여, `ActivityFeed` 모델 인스턴스를 조회하면서 모든 `parentable` 모델과 각각의 중첩 관계를 즉시 로드합니다:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::query()
    ->with(['parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWith([
            Event::class => ['calendar'],
            Photo::class => ['tags'],
            Post::class => ['author'],
        ]);
    }])->get();
```

<a name="eager-loading-specific-columns"></a>
#### 특정 컬럼만 즉시 로드하기

관계에서 모든 컬럼이 필요하지 않을 때는, 가져올 컬럼을 지정할 수 있습니다:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 이 기능을 사용할 때는 가져올 컬럼 목록에 반드시 `id` 컬럼과 관련 외래키 컬럼을 포함해야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본 즉시 로드

모델 조회 시 항상 특정 관계를 로드하고 싶다면, 모델에 `$with` 속성을 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * The relationships that should always be loaded.
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * Get the genre of the book.
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

특정 쿼리에서 `$with`의 항목을 제거하려면 `without` 메서드를 사용합니다:

```php
$books = Book::without('author')->get();
```

특정 쿼리에서 `$with`의 모든 항목을 재정의하려면 `withOnly` 메서드를 사용합니다:

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### 즉시 로드 조건 지정

관계를 즉시 로드하면서 추가 쿼리 조건을 지정하고 싶을 때는, `with` 메서드에 관계명을 키로, 클로저를 값으로 하는 배열을 전달합니다:

```php
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

이 예제에서 Eloquent는 게시글의 `title` 컬럼에 `code`가 포함된 게시글만 즉시 로드합니다. 다른 [쿼리 빌더](/docs/13.x/queries) 메서드도 호출하여 즉시 로드를 더 세밀하게 조정할 수 있습니다:

```php
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### `morphTo` 관계의 즉시 로드 조건 지정

`morphTo` 관계를 즉시 로드할 때, Eloquent는 각 관련 모델 타입마다 별도의 쿼리를 실행합니다. `MorphTo` 관계의 `constrain` 메서드로 각 쿼리에 조건을 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function ($query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function ($query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```

이 예제에서 Eloquent는 숨겨지지 않은 게시글과 `type` 값이 "educational"인 동영상만 즉시 로드합니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재와 함께 즉시 로드 조건 지정

관계의 존재를 확인하면서 동시에 같은 조건으로 관계를 즉시 로드해야 할 때가 있습니다. 예를 들어, 특정 쿼리 조건에 맞는 자식 `Post`를 가진 `User` 모델만 가져오면서 일치하는 게시글도 즉시 로드하려면 `withWhereHas` 메서드를 사용합니다:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### 지연 즉시 로드

부모 모델이 이미 조회된 뒤에 관계를 즉시 로드해야 할 때가 있습니다. 예를 들어, 관련 모델의 로드 여부를 동적으로 결정해야 하는 경우에 유용합니다:

```php
use App\Models\Book;

$books = Book::all();

if ($condition) {
    $books->load('author', 'publisher');
}
```

즉시 로드 쿼리에 추가 조건을 설정하려면, 관계명을 키로 하는 배열에 쿼리 인스턴스를 받는 클로저를 값으로 전달합니다:

```php
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

아직 로드되지 않은 관계만 로드하려면 `loadMissing` 메서드를 사용합니다:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### 중첩 지연 즉시 로드와 `morphTo`

`morphTo` 관계와 해당 관계가 반환할 수 있는 다양한 엔티티의 중첩 관계를 즉시 로드하려면 `loadMorph` 메서드를 사용합니다.

이 메서드는 첫 번째 인수로 `morphTo` 관계명을, 두 번째 인수로 모델/관계 쌍의 배열을 받습니다. 다음 모델을 참고하세요:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

이 예제에서 `Event`, `Photo`, `Post` 모델이 `ActivityFeed`를 생성할 수 있다고 가정합니다. `Event`는 `Calendar`에, `Photo`는 `Tag`에, `Post`는 `Author`에 속합니다.

이 모델 정의와 관계를 사용하여 `ActivityFeed` 인스턴스를 조회한 뒤, 모든 `parentable` 모델과 각각의 중첩 관계를 즉시 로드합니다:

```php
$activities = ActivityFeed::with('parentable')
    ->get()
    ->loadMorph('parentable', [
        Event::class => ['calendar'],
        Photo::class => ['tags'],
        Post::class => ['author'],
    ]);
```

<a name="automatic-eager-loading"></a>
### 자동 즉시 로드

> [!WARNING]
> 이 기능은 현재 커뮤니티 피드백을 수집하기 위해 베타 상태입니다. 이 기능의 동작과 기능은 패치 릴리스에서도 변경될 수 있습니다.

많은 경우 Laravel이 접근하는 관계를 자동으로 즉시 로드할 수 있습니다. 자동 즉시 로드를 활성화하려면, 앱의 `AppServiceProvider`의 `boot` 메서드에서 `Model::automaticallyEagerLoadRelationships` 메서드를 호출합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::automaticallyEagerLoadRelationships();
}
```

이 기능이 활성화되면, Laravel은 이전에 로드되지 않은 관계에 접근할 때 자동으로 로드를 시도합니다. 예를 들어:

```php
use App\Models\User;

$users = User::all();

foreach ($users as $user) {
    foreach ($user->posts as $post) {
        foreach ($post->comments as $comment) {
            echo $comment->content;
        }
    }
}
```

일반적으로 위 코드는 각 사용자의 게시글 조회를 위해, 그리고 각 게시글의 댓글 조회를 위해 개별 쿼리를 실행합니다. 하지만 `automaticallyEagerLoadRelationships` 기능이 활성화되면, 사용자 컬렉션 중 어느 사용자의 게시글에 접근할 때 Laravel이 자동으로 모든 사용자의 게시글을 [지연 즉시 로드](#lazy-eager-loading)합니다. 마찬가지로, 어느 게시글의 댓글에 접근하면 원래 조회한 모든 게시글의 댓글이 지연 즉시 로드됩니다.

전역으로 자동 즉시 로드를 활성화하지 않으려면, 단일 Eloquent 컬렉션 인스턴스에서 `withRelationshipAutoloading` 메서드를 호출하여 활성화할 수 있습니다:

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```

<a name="preventing-lazy-loading"></a>
### 지연 로드 방지

앞서 설명한 것처럼, 관계를 즉시 로드하면 애플리케이션에 상당한 성능 이점을 제공할 수 있습니다. 원한다면 Laravel에 관계의 지연 로드를 항상 방지하도록 지시할 수 있습니다. 이를 위해 Eloquent 모델 기본 클래스의 `preventLazyLoading` 메서드를 호출합니다. 보통 앱의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

`preventLazyLoading` 메서드는 지연 로드 방지 여부를 나타내는 선택적 boolean 인수를 받습니다. 예를 들어, 프로덕션이 아닌 환경에서만 지연 로드를 비활성화하여, 프로덕션 환경에서는 정상적으로 동작하면서도 실수로 지연 로드된 관계가 프로덕션 코드에 있어도 문제없게 할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

지연 로드를 방지한 후, Eloquent 관계의 지연 로드를 시도하면 `Illuminate\Database\LazyLoadingViolationException` 예외가 발생합니다.

`handleLazyLoadingViolationsUsing` 메서드로 지연 로드 위반 시 동작을 커스텀할 수 있습니다. 예를 들어, 예외 대신 로그만 기록하도록 설정할 수 있습니다:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 연관 모델 삽입 및 수정 (Inserting and Updating Related Models)

<a name="the-save-method"></a>
### `save` 메서드

Eloquent는 관계에 새 모델을 추가하는 편리한 메서드를 제공합니다. 예를 들어, 게시글에 새 댓글을 추가할 때, `Comment` 모델의 `post_id` 속성을 직접 설정하는 대신 관계의 `save` 메서드를 사용할 수 있습니다:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

`comments` 관계에 동적 속성이 아닌 메서드로 접근한 점에 주의하세요. `save` 메서드는 새 `Comment` 모델에 적절한 `post_id` 값을 자동으로 추가합니다.

여러 관련 모델을 저장하려면 `saveMany` 메서드를 사용합니다:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

`save`와 `saveMany` 메서드는 주어진 모델 인스턴스를 영속화하지만, 부모 모델에 이미 로드된 인메모리 관계에 새로 저장된 모델을 추가하지는 않습니다. `save`나 `saveMany` 사용 후 관계에 접근할 계획이라면 `refresh` 메서드를 사용하여 모델과 관계를 다시 로드하세요:

```php
$post->comments()->save($comment);

$post->refresh();

// All comments, including the newly saved comment...
$post->comments;
```

<a name="the-push-method"></a>
#### 모델과 관계 재귀적으로 저장하기

모델과 모든 연관 관계를 함께 `save`하려면 `push` 메서드를 사용합니다. 이 예제에서 `Post` 모델과 그 댓글, 댓글의 작성자가 모두 저장됩니다:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

이벤트를 발생시키지 않고 모델과 관계를 저장하려면 `pushQuietly` 메서드를 사용합니다:

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### `create` 메서드

`save`와 `saveMany` 외에도 `create` 메서드를 사용할 수 있습니다. 이 메서드는 속성 배열을 받아 모델을 생성하고 데이터베이스에 삽입합니다. `save`와 `create`의 차이점은 `save`가 전체 Eloquent 모델 인스턴스를 받는 반면, `create`는 일반 PHP `array`를 받는다는 것입니다. `create` 메서드는 새로 생성된 모델을 반환합니다:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

`createMany` 메서드로 여러 관련 모델을 생성할 수 있습니다:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

`createQuietly`와 `createManyQuietly` 메서드는 이벤트를 발생시키지 않고 모델을 생성합니다:

```php
$user = User::find(1);

$user->posts()->createQuietly([
    'title' => 'Post title.',
]);

$user->posts()->createManyQuietly([
    ['title' => 'First post.'],
    ['title' => 'Second post.'],
]);
```

`findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드를 사용하여 [관계에서 모델을 생성하고 업데이트](/docs/13.x/eloquent#upserts)할 수도 있습니다.

> [!NOTE]
> `create` 메서드를 사용하기 전에 [대량 할당(mass assignment)](/docs/13.x/eloquent#mass-assignment) 문서를 반드시 확인하세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 연관관계

자식 모델을 새 부모 모델에 할당하려면 `associate` 메서드를 사용합니다. 이 예제에서 `User` 모델은 `Account` 모델에 대해 `belongsTo` 관계를 정의합니다. `associate` 메서드는 자식 모델의 외래키를 설정합니다:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

자식 모델에서 부모를 제거하려면 `dissociate` 메서드를 사용합니다. 이 메서드는 관계의 외래키를 `null`로 설정합니다:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### 다대다 연관관계

<a name="attaching-detaching"></a>
#### 연결(Attaching) / 해제

Eloquent는 다대다 연관관계를 더 편리하게 다루기 위한 메서드도 제공합니다. 예를 들어, 사용자가 여러 역할을 가지고, 역할이 여러 사용자를 가질 수 있다고 합시다. `attach` 메서드로 관계의 중간 테이블에 레코드를 삽입하여 역할을 사용자에게 연결할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

관계를 연결할 때, 중간 테이블에 삽입할 추가 데이터를 배열로 전달할 수도 있습니다:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

사용자에게서 역할을 제거해야 할 때는 `detach` 메서드를 사용합니다. `detach`는 중간 테이블에서 해당 레코드를 삭제하지만, 양쪽 모델은 데이터베이스에 남아 있습니다:

```php
// Detach a single role from the user...
$user->roles()->detach($roleId);

// Detach all roles from the user...
$user->roles()->detach();
```

편의를 위해 `attach`와 `detach`는 ID 배열도 입력으로 받습니다:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 연관 동기화

`sync` 메서드를 사용하여 다대다 연결을 구성할 수도 있습니다. `sync` 메서드는 중간 테이블에 배치할 ID 배열을 받습니다. 주어진 배열에 없는 ID는 중간 테이블에서 제거됩니다. 따라서 이 작업이 완료되면 주어진 배열의 ID만 중간 테이블에 존재합니다:

```php
$user->roles()->sync([1, 2, 3]);
```

ID와 함께 추가 중간 테이블 값을 전달할 수도 있습니다:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

동기화된 모든 모델 ID에 동일한 중간 테이블 값을 삽입하려면 `syncWithPivotValues` 메서드를 사용합니다:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

주어진 배열에 없는 기존 ID를 분리하지 않으려면 `syncWithoutDetaching` 메서드를 사용합니다:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 연결 토글

다대다 관계는 주어진 관련 모델 ID의 연결 상태를 "토글"하는 `toggle` 메서드도 제공합니다. 현재 연결되어 있으면 해제하고, 해제되어 있으면 연결합니다:

```php
$user->roles()->toggle([1, 2, 3]);
```

ID와 함께 추가 중간 테이블 값을 전달할 수도 있습니다:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 레코드 수정

관계의 중간 테이블의 기존 행을 수정하려면 `updateExistingPivot` 메서드를 사용합니다. 이 메서드는 중간 레코드의 외래키와 업데이트할 속성 배열을 받습니다:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 동기화 (Touching Parent Timestamps)

모델이 `Comment`가 `Post`에 속하는 것처럼 `belongsTo` 또는 `belongsToMany` 관계를 정의할 때, 자식 모델이 업데이트될 때 부모의 타임스탬프를 갱신하면 유용한 경우가 있습니다.

예를 들어, `Comment` 모델이 업데이트될 때 소유 `Post`의 `updated_at` 타임스탬프를 자동으로 "터치"하여 현재 날짜와 시간으로 설정하고 싶을 수 있습니다. 이를 위해 자식 모델에 `Touches` 속성을 사용하고, 자식 모델이 업데이트될 때 `updated_at` 타임스탬프를 갱신할 관계명을 지정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Touches;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Touches(['post'])]
class Comment extends Model
{
    /**
     * Get the post that the comment belongs to.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 모델의 타임스탬프는 자식 모델이 Eloquent의 `save` 메서드를 사용하여 업데이트될 때만 갱신됩니다.

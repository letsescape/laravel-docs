# Eloquent: Relationships (Eloquent: 연관관계)

- [소개](#introduction)
- [연관관계 정의하기](#defining-relationships)
    - [일대일 / Has One](#one-to-one)
    - [일대다 / Has Many](#one-to-many)
    - [일대다 (역방향) / Belongs To](#one-to-many-inverse)
    - [여러 개 중 하나 (Has One of Many)](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [Scoped 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 조회](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 정렬](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [다형성 연관관계 (Polymorphic Relationships)](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 개 중 하나](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 Polymorphic 타입](#custom-polymorphic-types)
- [동적 연관관계](#dynamic-relationships)
- [연관관계 쿼리](#querying-relations)
    - [연관관계 메서드 vs 동적 속성](#relationship-methods-vs-dynamic-properties)
    - [연관관계 존재 여부 조회](#querying-relationship-existence)
    - [연관관계 부재 조회](#querying-relationship-absence)
    - [Morph To 연관관계 조회](#querying-morph-to-relationships)
- [연관 모델 집계](#aggregating-related-models)
    - [연관 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 연관관계에서 개수 세기](#counting-related-models-on-morph-to-relationships)
- [Eager Loading](#eager-loading)
    - [Eager Load 제약 조건](#constraining-eager-loads)
    - [Lazy Eager Loading](#lazy-eager-loading)
    - [자동 Eager Loading](#automatic-eager-loading)
    - [Lazy Loading 방지](#preventing-lazy-loading)
- [연관 모델 삽입 및 업데이트](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 연관관계](#updating-belongs-to-relationships)
    - [다대다 연관관계](#updating-many-to-many-relationships)
- [부모 모델 타임스탬프 갱신](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블은 서로 연관되어 있는 경우가 많습니다. 예를 들어 블로그 게시글에는 여러 개의 댓글이 있을 수 있고, 주문(order)은 해당 주문을 생성한 사용자와 연관될 수 있습니다.  

Eloquent는 이러한 연관관계를 관리하고 사용하는 작업을 매우 쉽게 만들어주며, 다음과 같은 다양한 형태의 일반적인 연관관계를 지원합니다.

<div class="content-list" markdown="1">

- [일대일 (One To One)](#one-to-one)
- [일대다 (One To Many)](#one-to-many)
- [다대다 (Many To Many)](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [일대일 (다형성)](#one-to-one-polymorphic-relations)
- [일대다 (다형성)](#one-to-many-polymorphic-relations)
- [다대다 (다형성)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의하기 (Defining Relationships)

Eloquent의 연관관계는 **Eloquent 모델 클래스 내부의 메서드**로 정의합니다.  

연관관계는 단순한 관계 정의뿐 아니라 강력한 [query builder](/docs/master/queries)의 기능도 함께 제공합니다. 따라서 연관관계를 메서드로 정의하면 메서드 체이닝(method chaining)을 통해 추가적인 쿼리 조건을 쉽게 붙일 수 있습니다.

예를 들어 `posts` 연관관계에 추가 조건을 연결할 수 있습니다.

```php
$user->posts()->where('active', 1)->get();
```

하지만 연관관계를 실제로 활용하기 전에, 먼저 Eloquent에서 지원하는 각 연관관계 유형을 어떻게 정의하는지 알아보겠습니다.

<a name="one-to-one"></a>
### 일대일 / Has One (One to One / Has One)

일대일 연관관계는 가장 기본적인 데이터베이스 관계 중 하나입니다.  

예를 들어 `User` 모델이 하나의 `Phone` 모델을 가질 수 있습니다. 이 관계를 정의하려면 `User` 모델에 `phone` 메서드를 추가합니다.

이 메서드는 `hasOne` 메서드를 호출하고 그 결과를 반환해야 합니다. `hasOne` 메서드는 모델의 기본 클래스인 `Illuminate\Database\Eloquent\Model`을 통해 사용할 수 있습니다.

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

`hasOne` 메서드의 첫 번째 인수는 연관된 모델 클래스 이름입니다.

연관관계를 정의한 후에는 **Eloquent의 동적 속성(dynamic property)** 을 사용하여 연관된 레코드를 가져올 수 있습니다.

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델 이름을 기반으로 **외래 키(foreign key)** 를 자동으로 추론합니다.

이 예제에서는 `Phone` 모델이 `user_id` 외래 키를 가지고 있다고 가정합니다.

이 규칙을 변경하고 싶다면 `hasOne` 메서드의 두 번째 인수로 외래 키를 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한 Eloquent는 기본적으로 외래 키 값이 부모 모델의 **기본 키(primary key)** 와 일치한다고 가정합니다.  

즉, `Phone.user_id` 컬럼에 `User.id` 값이 들어 있다고 가정합니다.

만약 `id`가 아닌 다른 컬럼을 사용하고 싶다면 세 번째 인수로 로컬 키(local key)를 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 역방향 연관관계 정의하기

이제 `User` 모델에서 `Phone` 모델에 접근할 수 있습니다.  

반대로 `Phone` 모델에서 해당 전화의 소유자인 `User`에 접근할 수 있도록 관계를 정의해보겠습니다.

`hasOne` 관계의 역방향은 `belongsTo` 메서드를 사용합니다.

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

`user` 메서드를 호출하면 Eloquent는 `Phone.user_id` 컬럼과 일치하는 `User.id` 값을 가진 모델을 찾습니다.

Eloquent는 관계 메서드 이름에 `_id`를 붙여 기본 외래 키 이름을 결정합니다.  

따라서 여기서는 `user_id` 컬럼이 사용됩니다.

외래 키가 다르다면 두 번째 인수로 지정할 수 있습니다.

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

또한 부모 모델의 기본 키가 `id`가 아니라면 세 번째 인수로 지정할 수 있습니다.

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / Has Many (One to Many / Has Many)

일대다 연관관계는 **하나의 부모 모델이 여러 개의 자식 모델을 가질 때** 사용합니다.

예를 들어 하나의 블로그 게시글에는 여러 개의 댓글이 있을 수 있습니다.

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

Eloquent는 `Comment` 모델의 외래 키를 자동으로 추론합니다.  

규칙은 **부모 모델 이름을 snake_case로 변환한 뒤 `_id`를 붙이는 것**입니다.

따라서 `comments` 테이블에는 `post_id` 컬럼이 있다고 가정합니다.

관계 정의 후에는 다음과 같이 컬렉션을 가져올 수 있습니다.

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

연관관계 역시 query builder 역할을 하기 때문에 추가 조건을 붙일 수도 있습니다.

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

외래 키와 로컬 키를 직접 지정할 수도 있습니다.

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 모델 자동 Hydration

Eager loading을 사용하더라도 **N + 1 쿼리 문제**가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 코드에서는 댓글을 eager load 했지만 `Comment`에서 `post`에 접근할 때 추가 쿼리가 발생합니다.

이 문제를 해결하려면 `hasMany` 정의 시 `chaperone`을 사용할 수 있습니다.

```php
public function comments(): HasMany
{
    return $this->hasMany(Comment::class)->chaperone();
}
```

또는 eager loading 시 적용할 수도 있습니다.

```php
$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다 (역방향) / Belongs To (One to Many Inverse)

이제 댓글에서 게시글로 접근하는 관계를 정의해보겠습니다.

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

이제 다음처럼 사용할 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

Eloquent는 기본적으로 `comments.post_id` 외래 키를 사용한다고 가정합니다.

필요하면 커스텀 키를 지정할 수 있습니다.

```php
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 키가 `id`가 아닌 경우:

```php
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델 (Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계는 관계가 `null`일 때 반환할 **기본 모델(default model)** 을 정의할 수 있습니다.

이 패턴은 **Null Object pattern**이라고 하며 조건문을 줄이는 데 도움이 됩니다.

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

속성을 지정할 수도 있습니다.

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}
```

또는 클로저를 사용할 수 있습니다.

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 연관관계 쿼리

일반적으로 다음처럼 쿼리할 수 있습니다.

```php
$posts = Post::where('user_id', $user->id)->get();
```

하지만 `whereBelongsTo`를 사용하는 것이 더 편리합니다.

```php
$posts = Post::whereBelongsTo($user)->get();
```

컬렉션도 전달할 수 있습니다.

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

관계 이름을 직접 지정할 수도 있습니다.

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

(문서가 매우 길어 응답 길이 제한에 도달했습니다. 필요하시면 **나머지 섹션(Has One of Many 이후 전체)** 도 동일한 방식으로 이어서 번역해 드리겠습니다.)
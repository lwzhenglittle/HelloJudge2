## 编译
编译参数中,```{extra}```为题目所提供的附加编译参数。

<table class="ui very basic celled table">
    <thead>
        <tr>
            <th>语言ID</th>
            <th>语言名</th>
            <th>编译参数</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>cpp</td>
            <td>C++</td>
            <td>g++ -Wall -Wextra  -fdiagnostics-color=never -DONLINE_JUDGE {source} -o {output} {extra}</td>
        </tr>
        <tr>
            <td>haskell</td>
            <td>Haskell</td>
            <td>ghc {source} -o {output} {extra}</td>
        </tr>
        <tr>
            <td>java8</td>
            <td>Java 8</td>
            <td>javac Main.java {extra}</td>
        </tr>
        <tr>
            <td>ocaml</td>
            <td>OCaml</td>
            <td>ocamlc -color never -custom str.cma -o {output} {source} {extra}</td>
        </tr>
        <tr>
            <td>rust</td>
            <td>Rust 1.33.0</td>
            <td>rustc -O -o {output} {source} {extra}</td>
        </tr>
    </tbody>
</table>

## 用户数据
### 个人信息
可以前往在登陆后进行个人资料的编辑。

个人简介支持```Markdown```与```KaTeX```。
### 头像
请前往[https://en.gravatar.com/](https://en.gravatar.com/)并使用自己的邮箱注册后上传头像。


## 题目与评测
管理员可以创建题目。

**由于Docker的限制，题目内存限制最少为4MB**

**暂不支持交互题与提交答案题**

点击创建题目按钮后会打开一个新的题目页面，点击右侧编辑后即可进行编辑。

题面支持```Markdown```与```LaTeX```，分别使用```Showdown```与```KaTeX```进行渲染。

Markdown语法可以参考[此处](https://github.com/showdownjs/showdown/wiki/Showdown's-Markdown-syntax).

题面数据中，样例部分使用HTML预格式化块（即不会被渲染Markdown或KaTex）。

题目未公开时，只有上传者和管理员才能访问此题。

公开后所有人均可访问。

**未公开的题目在题目列表中的字体颜色为绿色**

### Remote Judge

HJ2支持远程评测。

远程评测需要用户绑定相应OJ的账号，须提供明文密码。


### 题目数据
每个题目有自己所属的文件（类似于网盘），这些文件中可以公开某些文件提供给任何人下载（公开），也可以指定某些文件在编译用户程序时与程序放在一起（编译时提供）。


#### 子任务
每个题目可以设置若干子任务，评分以子任务为基础。

当一次提交中，不存在状态不为```unaccepted```的子任务后，即认为本题AC，所以题目满分可以不设置为100.

每个子任务可以指定自己的时限，内存限制，注释，名称等（会在题目页面上显示）。

HelloJudge2会自动分配子任务内每个测试点的得分，使其和为子任务的分数。

子任务的评分方式有两种，```sum```和```min```，前者会把一个子任务中所有测试点的分数加起来作为整个子任务的得分，后者只要子任务中有任意一个测试点没有通过即判为0分，否则即获得子任务全部分数。

为了便于修改，可以在题目数据处统一修改所有子任务的时限与空间限制。

**请尽可能地把子任务的数据范围写在子任务的说明里，而不是题面的提示里！！**

**请尽可能地把子任务的数据范围写在子任务的说明里，而不是题面的提示里！！**

**请尽可能地把子任务的数据范围写在子任务的说明里，而不是题面的提示里！！**

##### 快速生成子任务
可以使用JS的二维数组来快速生成子任务。
例如，指定输入文件名为```qwq#.in```,而输出文件名为```qwq#.out```，生成脚本填写以下代码时:
```javascript
[[1,2,3],[2,3,4],[3,4,5]]
```
会自动生成三个子任务，其中第一个子任务包含三个测试点，输入/输出文件分别为(qwq1.in,qwq1.out),(qwq2.in,qwq2.out),(qwq3.in,qwq3.out)
第二个，第三个以此类推。

生成脚本可以填写任意可以返回一个合法二维数组的表达式。

#### 附加编译参数

用来设定此题目所需的一些特殊编译参数(通常为指定C++标准或者优化开关),提交者可自行选择是否使用。

#### 重新生成文件列表

常用于手动修改了题目的数据目录后同步数据库。

点击后，HelloJudge2将会读取题目的数据目录下的文件并重新生成时间戳后存入数据库。

### 提交
一份代码提交后即会被加入到评测队列，由所有已注册评测机按照先来后到的原则进行评测。

HelloJudge2保证同一份提交的所有Subtask会在同一台评测机进行评测。

对于评测状态非```accepted```或```unaccepted```的提交，打开提交页面时会自动通过```Socket.io```实时更新评测信息。

### 测试数据与同步

可以在配置文件中选择是否使用自动同步测试数据。

如果使用自动同步测试数据，那么HelloJudge2与评测机会自动维护题目文件的时间戳，在每次评测开始时自动对比评测端与Web端的题目文件时间戳并自动下载过期文件。

如果不使用自动同步测试数据，那么请使用其他方式手动同步测试数据(例如```rsync```)。此选项常用与多个评测机实例共享一份数据目录时。

### SPJ
spj可以使用任何评测支持的语言编写。

spj程序的文件名应该为```spj_语言ID.xxx```，语言ID为```langs```文件夹下的语言ID，同时应该在题目数据页面指定SPJ文件名。


SPJ在运行时，目录下会有以下文件
- user_out: 用户在本测试点的输出
- input: 本测试点输入
- answer: 本测试点标准答案

SPJ应该创建以下两个文件:
- score: 本测试点得分(0~100,自动折合)
- message: (可选) 发送给用户的信息

#### 语言ID们

```cpp```,```haskell```,```java8```,```ocaml```,```python2```,```python3```,```rust```

### 从SYZOJ导入题目

HelloJudge2支持从SYZOJ导入题目，但是有以下注意事项：
- 不支持SYZOJ的交互题与提交答案题
- 暂不支持SYZOJ的附加文件格式

- 支持SYZOJ的子任务设定




## 提交记录
提交记录页面可以对提交记录进行筛选。

同时添加多个筛选器时，筛选器之间的关系为```AND```.

共有五个筛选器，见下表：
<table class="ui very basic celled table">
    <thead>
        <tr>
            <th>筛选器名</th>
            <th>取值</th>
            <th>作用</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>uid</td>
            <td>用户ID</td>
            <td>筛选所有指定用户的提交记录</td>
        </tr>
        <tr>
            <td>status</td>
            <td>accepted\unaccepted\judging\waiting</td>
            <td>筛选指定状态的提交记录</td>
        </tr>
        <tr>
            <td>min_score</td>
            <td>整数</td>
            <td>指定筛选的结果的最低分</td>
        </tr>
        <tr>
            <td>max_score</td>
            <td>整数</td>
            <td>指定筛选结果的最高分</td>
        </tr>
        <tr>
            <td>problem</td>
            <td>整数</td>
            <td>指定要筛选的题目ID</td>
        </tr>
        <tr>
            <td>contest</td>
            <td>整数</td>
            <td>筛选某次比赛的提交。设置为-1表示筛选非比赛提交</td>
        </tr>
    </tbody>
</table>

### 可见性
管理员可以看到所有的提交（包括比赛中的）。

非管理员只能看到所有的非比赛提交和自己在比赛中的提交。

## 团队

管理员可以创建团队。

任何人都可以加入或退出任何团队。

团队管理员或创建者可以修改团队的信息或者团队作业，或者将用户移出团队。

团队创建者可以设置团队管理员。

### 团队作业
团队作业为一组题目，团队内的成员关于这些题目的提交将会被显示在团队中并按照分数排名。

## 比赛

管理员可以创建比赛。

比赛描述支持Markdown与Latex。

暂不支持私有比赛。


开始时间与结束时间为ISO时间标准。

即```1926-08-17T12:34:56.000Z```表示****年\*月\*日12:34:56.000，UTC+0时区。

```1926-08-17T12:34:56+0800```表示****年\*月\*日,12:34:56.000,UTC+8时区（中国标准时间）

当```比赛时显示排行总榜```打开时，任何用户（包括比赛参加者），在比赛时都可以看到排行榜。

当```比赛时可以得知评测结果```打开时，任何用户都可以在比赛提交后得知自己的评测结果（而关闭时，评测状态为不可见。）


当排名依据为```题目最高得分```时，排行榜中，每个用户每道题目的最高分作为排行依据。

当排名依据为```最后一次提交```时，排行榜中，每个用户每道题目的最后一次提交将会被作为排行依据。

当排名依据为```罚时```时，所有用户首先按照通过的题目数量排名，通过题目数量的按照罚时从低到高排名。

一道题目的罚时为:题目AC时所经过的分钟数 + ```config.FAIL_SUBMIT_PENALTY``` * AC前失败提交次数。

一个用户的罚时为:所有AC题目罚时之和。

## 讨论
### 题目讨论
题目讨论可以直接通过题目页面进入并发表。

讨论支持Markdown与Latex。

### 全局讨论

讨论总版，闲聊灌水区?

### 题目全局讨论

可以认为是学术版。

### 置顶
管理员可以设置讨论置顶。

被置顶的讨论在任何情况下都会优先显示

### 公告

可以通过主页进入公告板块。

管理员可以发表公告。

### 其他

[所有讨论](/discussions/discussion/1)

[所有与题目有关的讨论](/discussions/discussion.problem/1)

## 权限系统

HelloJudge2具有权限系统。

每个用户属于一个唯一的权限组，自动拥有此权限组的所有权限。

同时每个用户也可以拥有自己的若干权限。

目前支持的权限如下表：

<table class="ui very basic celled table">
    <thead>
        <tr>
            <th>
                权限字符串
            </th>
            <th>
                说明
            </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                problem.create
            </td>
            <td>创建题目</td>
        </tr>
        <tr>
            <td>
                problem.publicize
            </td>
            <td>公开题目</td>
        </tr>
        <tr>
            <td>
                problem.manage
            </td>
            <td>
                题目管理(查看私有题，修改任意题目)
            </td>
        </tr>
        <tr>
            <td>
                submission.manage
            </td>
            <td>
                提交管理(查看私有提交，重测)
            </td>
        </tr>
        <tr>
            <td>
                contest.create
            </td>
            <td>
                创建比赛
            </td>
        </tr>
        <tr>
            <td>
                contest.publicize
            </td>
            <td>
                公开比赛(暂未实现)
            </td>
        </tr>
        <tr>
            <td>
                contest.manage
            </td>
            <td>
                管理任意比赛
            </td>
        </tr>
        <tr>
            <td>
                contest.use.比赛ID
            </td>
            <td>
                使用某场私有比赛(在正确输入私有比赛的邀请码之后，自动取得该权限)(暂未实现)
            </td>
        </tr>
        <tr>
            <td>
                permission.manage
            </td>
            <td>
                管理权限组，用户权限
            </td>
        </tr>
        <tr>
            <td>
                team.create
            </td>
            <td>
                创建团队
            </td>
        </tr>
        <tr>
            <td>
                team.manage
            </td>
            <td>
                团队管理 
            </td>
        </tr>
        <tr>
            <td>
                user.manage
            </td>
            <td>
                用户管理(修改用户个人信息等)
            </td>
        </tr>
        <tr>
            <td>
                discussion.manage
            </td>
            <td>
                讨论管理
            </td>
        </tr>
        <tr>
            <td>
                backend.manage
            </td>
            <td>
                后台管理
            </td>
        </tr>
        <tr>
            <td>
                remote_judge.use
            </td>
            <td>
                使用远程评测
            </td>
        </tr>
        <tr>
            <td>
                problemset.create
            </td>
            <td>
                创建习题集
            </td>
        </tr>
        <tr>
            <td>
                problemset.use.ID
            </td>
            <td>
                使用某个私有习题集
            </td>
        </tr>
        <tr>
            <td>
                problemset.use.public
            </td>
            <td>
                使用公共习题集
            </td>
        </tr>
        <tr>
            <td>
                problemset.manage
            </td>
            <td>
                管理习题集
            </td>
        </tr>
    </tbody>
</table>


### 权限的认定规则
当判断一个用户有没有权限a.b.c.d时,按照以下优先级进行计算:

(下文中的用户权限均指用户所属的组的权限与用户自身权限的并集)

1. 如果用户拥有权限-a.b.c.d,则认为用户**没有**权限a.b.c.d
2. 如果用户有a.b.c.d权限时,则认为用户拥有权限a.b.c.d
3. 如果用户有以下权限之一时,则认为用户拥有权限a.b.c.d
- \*
- a.*
- a.b.*
- a.b.c.*
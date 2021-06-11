import Mock from 'mockjs';
const vehicle = Mock.mock(
    '/api/car', 'post', (req, res) => {
        return {
            code: 200,
            data: [{
                id: 1,
                name: 'BYD',

            }, {
                id: 1,
                name: 'baojun',
            }],
            message: '查询成功'
        }
    })

const user = Mock.mock(
    '/api/user', 'get', (req, res) => {
        return {
            code: 200,
            data: {
                id: 1,
                sex: 1,
                age: 25,
                createTime: '2017-04-01'
            },
            message: '查询成功'
        }
    })


const test = Mock.mock(
    '/api/test', 'get', (req, res) => {
        return {
            items: [{
                id: 1,
                timestamp: 758411980101,
                author: 'Angela',
                reviewer: 'Daniel',
                title: 'Msq Egfr Qber Mqbdbpyh Lnerdq Viij Odiwfbg Ibhi',
                content_short: 'mock data',
                content: '<p>I am testing data, I am testing data.</p><p><img src=\"https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943\"></p>',
                forecast: 45.74,
                importance: 2,
                type: 'JP',
                status: 'published',
                display_time: '1975-04-30 21:38:05',
                comment_disabled: true,
                pageviews: 2835,
                image_uri: 'https://wpimg.wallstcn.com/e4558086-631c-425c-9430-56ffb46e70b3',
                platforms: [
                    'a-platform'
                ],
                edit: false,
                originalTitle: 'Msq Egfr Qber Mqbdbpyh Lnerdq Viij Odiwfbg Ibhi'
            }]
        }
    })

export default {
    tset,
    vehicle,
    user
}
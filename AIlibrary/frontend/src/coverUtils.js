const categoryCovers = {
  科幻: [
    'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600&q=80',
    'https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=600&q=80',
    'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=600&q=80'
  ],
  文学: [
    'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&q=80',
    'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=600&q=80',
    'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=600&q=80'
  ],
  历史: [
    'https://images.unsplash.com/photo-1461360228754-6e81c478b882?w=600&q=80',
    'https://images.unsplash.com/photo-1471107340929-a87cd0f5b5f3?w=600&q=80'
  ],
  哲学: [
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=80',
    'https://images.unsplash.com/photo-1535905557558-afc3357fa9f3?w=600&q=80'
  ],
  编程: [
    'https://images.unsplash.com/photo-1515879218367-8466d910auj9?w=600&q=80',
    'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600&q=80',
    'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600&q=80'
  ],
  经济: [
    'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&q=80',
    'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&q=80'
  ],
  心理: [
    'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=600&q=80',
    'https://images.unsplash.com/photo-1559757175-5700dde675bc?w=600&q=80'
  ],
  推理: [
    'https://images.unsplash.com/photo-1519074069444-1ba4fff66d16?w=600&q=80',
    'https://images.unsplash.com/photo-1587876936092-f1e0744d9306?w=600&q=80'
  ],
  治愈: [
    'https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=600&q=80',
    'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c5?w=600&q=80',
    'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=600&q=80'
  ],
  自然: [
    'https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=600&q=80',
    'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&q=80'
  ],
  艺术: [
    'https://images.unsplash.com/photo-1549887552-cb1071d3e5ca?w=600&q=80',
    'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=600&q=80'
  ]
}

const defaultCovers = [
  'https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=600&q=80',
  'https://images.unsplash.com/photo-1550399105-c4eb705e46ce?w=600&q=80',
  'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600&q=80',
  'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=600&q=80',
  'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=600&q=80'
]

const tagToCategory = {
  '科幻': '科幻', '科普': '科幻', '宇宙': '科幻', '太空': '科幻', '外星': '科幻',
  '文学': '文学', '小说': '文学', '经典': '文学', '童话': '文学', '诗歌': '文学', '散文': '治愈',
  '历史': '历史', '传记': '历史', '考古': '历史', '文明': '历史',
  '哲学': '哲学', '思想': '哲学', '伦理': '哲学', '宗教': '哲学',
  '编程': '编程', '计算机': '编程', '技术': '编程', 'Python': '编程', 'Java': '编程', '算法': '编程', '人工智能': '编程',
  '经济': '经济', '商业': '经济', '管理': '经济', '金融': '经济',
  '心理': '心理', '情绪': '心理', '思维': '心理', '认知': '心理',
  '推理': '推理', '悬疑': '推理', '侦探': '推理', '犯罪': '推理',
  '治愈': '治愈', '温情': '治愈', '温暖': '治愈', '成长': '治愈',
  '自然': '自然', '旅行': '自然', '户外': '自然', '生态': '自然',
  '艺术': '艺术', '美学': '艺术', '建筑': '艺术', '设计': '艺术', '音乐': '艺术'
}

function hashString(str) {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  return Math.abs(hash)
}

export function getBookCover(title, tags) {
  if (!title) return defaultCovers[0]

  let category = null
  if (tags && Array.isArray(tags)) {
    for (const tag of tags) {
      const cat = tagToCategory[tag]
      if (cat && categoryCovers[cat]) {
        category = cat
        break
      }
    }
  }

  // 兜底：尝试从标题匹配
  if (!category) {
    for (const [keyword, cat] of Object.entries(tagToCategory)) {
      if (title.includes(keyword)) {
        category = cat
        break
      }
    }
  }

  const covers = category ? categoryCovers[category] : defaultCovers
  const index = hashString(title) % covers.length
  return covers[index]
}

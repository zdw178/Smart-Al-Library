-- 在 Supabase SQL Editor 中运行此文件
-- https://tesgvfyvhwaavqoxmbah.supabase.co → SQL Editor

-- 创建搜索记录表
CREATE TABLE IF NOT EXISTS ai_search_sessions (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  search_query TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 允许 anon 角色插入数据（RLS 策略）
ALTER TABLE ai_search_sessions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "允许匿名用户插入搜索记录" ON ai_search_sessions;
CREATE POLICY "允许匿名用户插入搜索记录" ON ai_search_sessions
  FOR INSERT
  TO anon
  WITH CHECK (true);

-- 允许 anon 角色读取自己的数据（可选，供管理后台使用）
DROP POLICY IF EXISTS "允许匿名用户读取搜索记录" ON ai_search_sessions;
CREATE POLICY "允许匿名用户读取搜索记录" ON ai_search_sessions
  FOR SELECT
  TO anon
  USING (true);

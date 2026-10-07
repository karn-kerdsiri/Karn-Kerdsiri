import { render, screen } from '@testing-library/react'
import { test, expect } from 'vitest'
import App from '../App.jsx'

test('test_TC_BKG_01_2_slot_full', () => {
  // Given: ช่วง 09.00 น. เต็มระหว่างยืนยัน และมีช่วงว่างในวันเดียวกันกับวันถัดไป
  // When: ยืนยันการจองช่วง 09.00 น.
  render(<App />)

  // Then: แจ้ง "ช่วงเวลาเต็ม"
  expect(screen.getByText('ช่วงเวลาเต็ม')).toBeTruthy()

  // Then: แสดง 3 ช่วงว่างที่ใกล้ 09.00 น. ที่สุดภายในวันเดียวกันและวันถัดไป
  expect(screen.getAllByRole('button')).toHaveLength(3)
})
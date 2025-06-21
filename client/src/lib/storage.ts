
const RECENT_LOOKUPS_KEY = 'layoff-radar-recent-lookups';
const MAX_RECENT_LOOKUPS = 5;

export const getRecentLookups = (): string[] => {
  try {
    const stored = localStorage.getItem(RECENT_LOOKUPS_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
};

export const saveToRecentLookups = (company: string): string[] => {
  try {
    const recent = getRecentLookups();
    const filtered = recent.filter(item => item.toLowerCase() !== company.toLowerCase());
    const updated = [company, ...filtered].slice(0, MAX_RECENT_LOOKUPS);
    
    localStorage.setItem(RECENT_LOOKUPS_KEY, JSON.stringify(updated));
    return updated;
  } catch {
    return [company];
  }
};

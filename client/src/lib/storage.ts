const RECENT_LOOKUPS_KEY = 'farsight_recent_lookups';
const MAX_RECENT_LOOKUPS = 5;

export const getRecentLookups = (): string[] => {
  try {
    const item = window.localStorage.getItem(RECENT_LOOKUPS_KEY);
    return item ? JSON.parse(item) : [];
  } catch (error) {
    console.error('Error reading recent lookups from localStorage', error);
    return [];
  }
};

export const saveToRecentLookups = (company: string): string[] => {
  if (!company) return getRecentLookups();

  try {
    const recent = getRecentLookups();
    const normalizedCompany = company.toLowerCase();
    
    // Remove if it already exists to move it to the front
    const filtered = recent.filter(r => r.toLowerCase() !== normalizedCompany);
    
    // Add the new company to the front
    const updated = [company, ...filtered];
    
    // Trim to the max allowed
    const final = updated.slice(0, MAX_RECENT_LOOKUPS);

    window.localStorage.setItem(RECENT_LOOKUPS_KEY, JSON.stringify(final));
    return final;
  } catch (error) {
    console.error('Error saving recent lookups to localStorage', error);
    return getRecentLookups();
  }
};
